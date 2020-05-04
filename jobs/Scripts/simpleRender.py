import argparse
import os
import subprocess
import psutil
import json
import ctypes
import pyscreenshot
import platform
from datetime import datetime
from shutil import copyfile, move, which
import sys
import re
import time

sys.path.append(os.path.abspath(os.path.join(
	os.path.dirname(__file__), os.path.pardir, os.path.pardir)))

import jobs_launcher.core.config as core_config
from jobs_launcher.core.system_info import get_gpu
from jobs_launcher.core.kill_process import kill_process


def createArgsParser():
	parser = argparse.ArgumentParser()

	parser.add_argument('--tool', required=True, metavar="<dir>")
	parser.add_argument('--output', required=True, metavar="<dir>")
	parser.add_argument('--testType', required=True)
	parser.add_argument('--test_list', required=True)
	parser.add_argument('--res_path', required=False, default=120)

	return parser


def main(args):
	args = createArgsParser().parse_args()

	cases_list = []
	try:
		with open(os.path.join(os.path.dirname(sys.argv[0]), args.test_list)) as f:
			cases_list = json.load(f)
		core_config.main_logger.info("Cases: {}".format([name['case'] for name in cases_list]))
	except OSError as e:
		core_config.main_logger.error("Failed to read test cases json. ")
		core_config.main_logger.error(str(e))
		exit(-1)

	core_config.main_logger.info("Cases")
	core_config.main_logger.info(cases_list)

	core_config.main_logger.info('Create empty report files')

	gpu = get_gpu()
	if not gpu:
		core_config.main_logger.error("Can't get gpu name")
	process_platform = {platform.system(), gpu}

	args.tool = os.path.abspath(args.tool)
	tool_path = os.path.dirname(args.tool)
	work_dir = os.path.abspath(args.output)
	result_path = os.path.join(work_dir, 'Output')
	if not os.path.exists(result_path):
		os.makedirs(result_path)

	'''
	for case in cases_list:
		if sum([process_platform & set(skip_conf) == set(skip_conf) for skip_conf in case.get('skip_on', '')]):
			for i in case['skip_on']:
				skip_on = set(i)
				if process_platform.intersection(skip_on) == skip_on:
					case['status'] = 'skipped'

		if case['status'] != 'done':
			if case["status"] == 'inprogress':
				case['status'] = 'active'
				case['number_of_tries'] = case.get('number_of_tries', 0) + 1

			template = core_config.RENDER_REPORT_BASE
			template['test_case'] = case['case']
			template['process_device'] = get_gpu()
			template['test_status'] = 'error'
			template['script_info'] = case['script_info']
			# TODO: add input files info
			template['test_group'] = args.testType
			template['date_time'] = datetime.now().strftime(
				'%m/%d/%Y %H:%M:%S')

			with open(os.path.join(work_dir, case['case'] + core_config.CASE_REPORT_SUFFIX), 'w') as f:
				f.write(json.dumps([template], indent=4))
	'''

	with open(os.path.join(work_dir, 'test_cases.json'), "w+") as f:
		json.dump(cases_list, f, indent=4)

	system_pl = platform.system()

	for case in cases_list:
		command_args = case["command_args"]
		execute_file = case["tool"]

		core_config.main_logger.info(command_args)
		command_args = command_args.format(RES_PATH=args.res_path, OUTPUT=result_path)
		core_config.main_logger.info(command_args)

		if system_pl == "Windows":
			cmdRun = "{tool}.exe {command_args}".format(tool=args.tool, command_args=command_args)
			cmdScriptPath = os.path.join(work_dir, 'script.bat')
			with open(cmdScriptPath, 'w') as f:
				f.write(cmdRun)
		else:
			cmdRun = "./{tool} {command_args}".format(tool=args.tool, command_args=command_args)
			cmdScriptPath = os.path.join(work_dir, 'script.sh')
			with open(cmdScriptPath, 'w') as f:
				f.write(cmdRun)
			os.system('chmod +x {}'.format(cmdScriptPath))

		core_config.main_logger.info('Launch script on {tool} ({path})'.format(tool=case["tool"], path=cmdScriptPath))

		os.chdir(args.output)
		p = psutil.Popen(cmdScriptPath, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		rc = 1

		try:
			stdout, stderr = p.communicate(timeout=180)
		except (psutil.TimeoutExpired, subprocess.TimeoutExpired) as err:
			core_config.main_logger.error("Process has been aborted by timeout")
			rc = -1
			for child in reversed(p.children(recursive=True)):
				child.terminate()
			p.terminate()
		finally:

			with open("tool_log.txt", 'a', encoding='utf-8') as file:
				stdout = stdout.decode("utf-8")
				file.write(stdout)

			with open("tool_log.txt", 'a', encoding='utf-8') as file:
				file.write("\n ----STEDERR---- \n")
				stderr = stderr.decode("utf-8")
				file.write(stderr)


if __name__ == "__main__":

	core_config.main_logger.info("simpleProcess start working...")
	args = createArgsParser().parse_args()
	exit(main(args))
