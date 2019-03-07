#coding:utf-8
import os
import argparse
from VideoTools.VUtils import VUtils, Report

default_target = os.path.abspath('.')
parser = argparse.ArgumentParser()
parser.add_argument("-q", "--quiet", action="store_true", help="命令行模式")#python VideoScan.py -q

# 互斥参数
g = parser.add_mutually_exclusive_group()
g.add_argument("-c", "--compare", action="store_true", help="视频参数比对模式")
g.add_argument("-i", "--info", action="store_true", help="视频参数查看模式")

parser.add_argument("-f", "--file", help="视频文件 或 视频文件路径")
parser.add_argument("-t", "--target", default=default_target, help="报告生成路径")
args = parser.parse_args()


class HtmlBuilder:
    @staticmethod
    def detail_build(file, target):
        img_path = os.path.join(target, 'img')#帧图片的目录
        os.makedirs(img_path, exist_ok=True)#创建图片存放的目录
        VUtils.output_frame(file, img_path, 'I')#输出I帧
        VUtils.output_frame(file, img_path, 'P')#输出P帧
        frame_info, index_info = VUtils.get_img_idx(file)#初始化帧的信息和编号
        Report.echo_theme_js(target)#输出theme.js到文件夹
        Report.echo_info_html(target)#输出info.html到文件夹
        Report.echo_info_frame_js(target)#输出frame.js到文件夹
        Report.echo_info_data(target, frame_info, index_info)#输出data文件

    @staticmethod
    def cmpare_build(file, target):
        files = os.listdir(file)#方法用于返回指定的文件夹包含的文件或文件夹的名字的列表
        mp4_files = [i for i in files if i[-4:].upper() == '.MP4']#初始化MP4的文件名
        # for i in mp4_files:
        #     res.append(VUtils.get_stream_arg(os.path.join(file, i)))  # 拼接竞品名字
        res = [VUtils.get_stream_arg(os.path.join(file, i)) for i in mp4_files]  # 拼接竞品名字
        product = mp4_files
        radar_title = {
            'text': '视频信息雷达图',
            'subtext': '同个视频不同竞品参数对比分析'
        }
        radar_indicator = [
            {'text': 'video时长', 'max': 60, 'color': 'red'},
            {'text': '视频码率kbps', 'max': 5, 'color': 'red'},
            {'text': 'B帧信息', 'max': 5, 'color': 'red'},
            {'text': '实际帧率', 'max': 100, 'color': 'red'},
            {'text': '帧数', 'max': 2000, 'color': 'red'},
            {'text': 'audio时长', 'max': 60, 'color': 'green'},
            {'text': '音频采样率', 'max': 3000, 'color': 'green'},
        ]
        radar_data = []
        for idx, i in enumerate(res):
            video_duration = round(eval(i['vedio']['duration']), 2)
            audio_duration = round(eval(i['audio']['duration']) if 'audio' in i.keys() else 0, 2)
            audio_nb_frames = i['audio']['nb_frames'] if 'audio' in i.keys() else 0
            video_bit_rate = round(int(i['vedio']['bit_rate']) / 1024 / 1024, 2)
            video_nb_frames = i['vedio']['nb_frames']
            video_b_frames = i['vedio']['b_frames']
            video_r_frame_rate = eval(i['vedio']['r_frame_rate'])
            # 0 - video时长  # 1 - 视频码率  2 -B帧信息   3 - 实际帧率  4 - 帧数  5 - audio时长  6 - 音频采样率
            l = [video_duration, video_bit_rate, video_b_frames, video_r_frame_rate, video_nb_frames, audio_duration, audio_nb_frames]
            radar_data.append({'value': l, 'name': product[idx]})
            # print(radar_data)
        # 0 - video时长  # 1 - 视频码率  2 -B帧信息   3 - 实际帧率  4 - 帧数  5 - audio时长  6 - 音频采样率
        bar_settings = [
            {
                'title': {
                    'text': "video时长",
                    'subtext': "同个视频不同竞品video时长分析"
                },
                'name': "video时长",
                'data': [i['value'][0] for i in radar_data]
            },
            {
                'title': {
                    'text': "视频码率kbps",
                    'subtext': "同个视频不同竞品视频码率分析"
                },
                'name': "LALALA",
                'data': [i['value'][1] for i in radar_data]
            },
            {
                'title': {
                    'text': "B帧信息",
                    'subtext': "同个视频查看是否有B帧存在"
                },
                'name': "LALALA",
                'data': [i['value'][2] for i in radar_data]
            },
            {
                'title': {
                    'text': "实际帧率",
                    'subtext': "同个视频不同竞品实际帧率分析"
                },
                'name': "LALALA",
                'data': [i['value'][3] for i in radar_data]
            },
            {
                'title': {
                    'text': "帧数",
                    'subtext': "同个视频不同竞品帧数量分析"
                },
                'data': [i['value'][4] for i in radar_data]
            },
            {
                'title': {
                    'text': "audio时长",
                    'subtext': "同个视频不同竞品audio时长分析"
                },
                'name': "I帧",
                'data': [i['value'][5] for i in radar_data]
            },
            {
                'title': {
                    'text': "音频采样率",
                    'subtext': "同个视频不同竞品音频采样率分析"
                },
                'name': "LALALA",
                'data': [i['value'][6] for i in radar_data]
            },
        ]
        Report.echo_cmp_html(target)
        Report.echo_theme_js(target)
        Report.echo_cmp_frame_js(target)
        Report.echo_cmp_data(target, product, radar_title, radar_indicator, radar_data, bar_settings)


if not args.quiet:
    mode, file, target = '', '', ''
    while mode not in ('1', '2'):
        mode = input("请选择操作：1,视频对比\t2,视频信息查看:\n(1 or 2)")
    while not os.path.exists(file):
        file = input("请输入文件路径or文件名:\n")
    while not os.path.isdir(target):
        target = input("请输入报告生成路径:\n")
    print(mode, file, target)
    if mode == '1':
        HtmlBuilder.cmpare_build(file, target)
    else:
        HtmlBuilder.detail_build(file, target)
else:
    print("命令行模式")
    if not (args.compare or args.info):
        print("缺少必要参数，请选择模式:(-c or -i)")
    elif args.compare:
        if args.file:
            print("视频对比模式")
            target, file = args.target, args.file
            HtmlBuilder.cmpare_build(file, target)
        else:
            print("缺少必要参数，请输入：-f 视频所在目录")
    else:
        if args.file:
            print("视频信息查看模式")
            target, file = args.target, args.file
            HtmlBuilder.detail_build(file, target)
        else:
            print("缺少必要参数，请输入：-f 视频文件路径")
