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

ROOT_DIR = os.path.abspath(os.path.join(
	os.path.dirname(__file__), os.path.pardir, os.path.pardir))
PROCESS = ['TALibDopplerTest.exe', 'TALibTestConvolution.exe', 'TALibDopplerTest', 'TALibTestConvolution', 'talibdopplertest', 'talibtestconvolution']


def createArgsParser():
	parser = argparse.ArgumentParser()

	parser.add_argument('--output', required=True, metavar="<dir>")
	parser.add_argument('--testType', required=True)
	parser.add_argument('--res_path', required=True)
	parser.add_argument('--pass_limit', required=True)
	parser.add_argument('--testCases', required=True)
	parser.add_argument('--error_count', required=False, default=0, type=int)

	return parser


def main(args):
	try:
		with open(os.path.join(os.path.dirname(__file__), 'base_functions.py')) as f:
			script = f.read()
	except OSError as e:
		core_config.main_logger.error(str(e))
		return 1

	if os.path.exists(os.path.join(os.path.dirname(__file__), 'extensions', args.testType + '.py')):
		with open(os.path.join(os.path.dirname(__file__), 'extensions', args.testType + '.py')) as f:
			extension_script = f.read()
		script = script.split('# place for extension functions')
		script = script[0] + extension_script + script[1]

	work_dir = os.path.abspath(args.output)
	script = script.format(work_dir=work_dir, testType=args.testType, render_device=args.render_device, res_path=args.res_path, pass_limit=args.pass_limit,
						   resolution_x=args.resolution_x, resolution_y=args.resolution_y, SPU=args.SPU, threshold=args.threshold)

	with open(os.path.join(args.output, 'base_functions.py'), 'w') as file:
		file.write(script)

	if (os.path.exists(args.testCases) and '.json' in args.testCases):
		with open(os.path.join(args.testCases)) as f:
			tc = f.read()
			test_cases = json.loads(tc)[args.testType]
		necessary_cases = [
			item for item in cases if item['case'] in test_cases]
		cases = necessary_cases

	core_config.main_logger.info('Create empty report files')

	if not os.path.exists(os.path.join(work_dir, 'Color')):
		os.makedirs(os.path.join(work_dir, 'Color'))
	copyfile(os.path.abspath(os.path.join(work_dir, '..', '..', '..', '..', 'jobs_launcher',
										  'common', 'img', 'error.jpg')), os.path.join(work_dir, 'Color', 'failed.jpg'))

	gpu = get_gpu()
	if not gpu:
		core_config.main_logger.error("Can't get gpu name")
	render_platform = {platform.system(), gpu}

	for case in cases:
		if sum([render_platform & set(skip_conf) == set(skip_conf) for skip_conf in case.get('skip_on', '')]):
			for i in case['skip_on']:
				skip_on = set(i)
				if render_platform.intersection(skip_on) == skip_on:
					case['status'] = 'skipped'

		if case['status'] != 'done':
			if case["status"] == 'inprogress':
				case['status'] = 'active'
				case['number_of_tries'] = case.get('number_of_tries', 0) + 1

			template = core_config.RENDER_REPORT_BASE
			template['test_case'] = case['case']
			template['render_device'] = get_gpu()
			template['test_status'] = 'error'
			template['script_info'] = case['script_info']
			template['scene_name'] = case.get('scene', '')
			template['file_name'] = 'failed.jpg'
			template['render_color_path'] = os.path.join('Color', 'failed.jpg')
			template['test_group'] = args.testType
			template['date_time'] = datetime.now().strftime(
				'%m/%d/%Y %H:%M:%S')

			with open(os.path.join(work_dir, case['case'] + core_config.CASE_REPORT_SUFFIX), 'w') as f:
				f.write(json.dumps([template], indent=4))

	with open(os.path.join(work_dir, 'test_cases.json'), "w+") as f:
		json.dump(cases, f, indent=4)

	cmdRun = '"{tool}" -b -P "{template}"\n'.format(
		tool=args.tool, template=os.path.join(args.output, 'base_functions.py'))

	system_pl = platform.system()
	if system_pl == "Windows":
		cmdScriptPath = os.path.join(work_dir, 'script.bat')
		with open(cmdScriptPath, 'w') as f:
			f.write(cmdRun)
	else:
		cmdScriptPath = os.path.join(work_dir, 'script.sh')
		with open(cmdScriptPath, 'w') as f:
			f.write(cmdRun)
		os.system('chmod +x {}'.format(cmdScriptPath))

	core_config.main_logger.info('Launch script on Blender ({})'.format(cmdScriptPath))

	p = subprocess.Popen(cmdScriptPath, shell=True,
						 stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	stdout, stderr = p.communicate()

	with open(os.path.join(args.output, "renderTool.log"), 'a', encoding='utf-8') as file:
		stdout = stdout.decode("utf-8")
		file.write(stdout)

	with open(os.path.join(args.output, "renderTool.log"), 'a', encoding='utf-8') as file:
		file.write("\n ----STEDERR---- \n")
		stderr = stderr.decode("utf-8")
		file.write(stderr)

	try:
		rc = p.wait(timeout=100)
	except psutil.TimeoutExpired as err:
		rc = -1
		for child in reversed(p.children(recursive=True)):
			child.terminate()
		p.terminate()

	# TODO: check athena work in blender

	return rc


def group_failed(args):
	try:
		cases = json.load(open(os.path.realpath(
			os.path.join(os.path.abspath(args.output), 'test_cases.json'))))
	except Exception as e:
		core_config.logging.error("Can't load test_cases.json")
		core_config.main_logger.error(str(e))
		exit(-1)

	for case in cases:
		if case['status'] == 'active':
			case['status'] = 'skipped'

	with open(os.path.join(os.path.abspath(args.output), 'test_cases.json'), "w+") as f:
		json.dump(cases, f, indent=4)

	rc = main(args)
	kill_process(PROCESS)
	core_config.main_logger.info(
		"Finish simpleRender with code: {}".format(rc))
	exit(rc)


if __name__ == "__main__":
	core_config.main_logger.info("simpleRender start working...")
	
	args = createArgsParser().parse_args()

	iteration = 0

	try:
		os.makedirs(args.output)
	except OSError as e:
		pass
	
	try:
		copyfile(os.path.realpath(os.path.join(os.path.dirname(
					__file__), '..', 'Tests', args.testType, 'test_cases.json')),
				os.path.realpath(os.path.join(os.path.abspath(
					args.output), 'test_cases.json')))
	except:
		core_config.logging.error("Can't copy test_cases.json")
		core_config.main_logger.error(str(e))
		exit(-1)

	while True:
		iteration += 1

		core_config.main_logger.info(
			'Try to run script in blender (#' + str(iteration) + ')')

		rc = main(args)

		try:
			move(os.path.join(os.path.abspath(args.output), 'renderTool.log'),
				 os.path.join(os.path.abspath(args.output), 'renderTool' + str(iteration) + '.log'))
		except:
			core_config.main_logger.error('No renderTool.log')

		try:
			cases = json.load(open(os.path.realpath(
				os.path.join(os.path.abspath(args.output), 'test_cases.json'))))
		except Exception as e:
			core_config.logging.error("Can't load test_cases.json")
			core_config.main_logger.error(str(e))
			exit(-1)

		active_cases = 0
		current_error_count = 0

		for case in cases:
			if case['status'] in ['fail', 'error', 'inprogress']:
				current_error_count += 1
				if args.error_count == current_error_count:
					group_failed(args)
			else:
				current_error_count = 0

			if case['status'] in ['active', 'fail', 'inprogress']:
				active_cases += 1

		if active_cases == 0 or iteration > len(cases) * 2:	# 2- retries count		
			# exit script if base_functions don't change number of active cases
			kill_process(PROCESS)
			core_config.main_logger.info(
				"Finish simpleRender with code: {}".format(rc))
			exit(rc)