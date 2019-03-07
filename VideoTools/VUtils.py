# coding:utf-8
import os
import json

import locale
print(locale.getdefaultlocale())
"""
os.popen(cmd, 'r', 1).read()
"""


class VUtils:
    '''
    检查是否安装ffprobe
    '''
    print('执行环境检查...')
    cmd = 'ffprobe -version'
    res = os.popen(cmd, 'r', 1).read()
    if 'version' not in res:
        raise EnvironmentError('no ffprobe found, see https://www.ffmpeg.org/')
    print('环境检查通过')
    @staticmethod
    def get_all_frames(filepath):
        cmd = 'ffprobe -v quiet -show_frames -of json %s' % filepath#拿到到每一帧的数据
        res = os.popen(cmd, 'r', 1).read()
        res = json.loads(res)
        return res.get('frames', '')

    @staticmethod
    def get_video_info(filepath):
        cmd = 'ffprobe -v quiet -show_streams -of json %s' % filepath#整段视频的数据（video和audio）
        res = os.popen(cmd, 'r', 1).read()
        res = json.loads(res)
        return res.get('streams', '')

    @staticmethod
    def output_frame(filepath, target, ftype):#拿到i/p/b帧的图片
        ftype = ftype.upper()
        if ftype in ('I', 'P', 'B'):
            cmd = "ffmpeg -v quiet -i %s -vf select='eq(pict_type\,%s)' -vsync 2 -f image2 %s/%s%%d.jpg" % (filepath, ftype, target, ftype)
            res = os.popen(cmd, 'r', 1).read()
            print(res)
        else:
            raise ValueError('ftype should be I/P/B')

    @staticmethod
    def get_img_idx(filepath):#判断是video时，输出i、P帧的帧号
        frame_info = VUtils.get_all_frames(filepath)
        index_info, i_idx, p_idx = {}, 1, 1
        for idx, val in enumerate(frame_info):
            if val['media_type'] == 'audio':
                continue
            if val['pict_type'] == 'I':
                index_info[str(idx)] = 'I%s.jpg' % i_idx
                i_idx += 1
            elif val['pict_type'] == 'P':
                index_info[str(idx)] = 'P%s.jpg' % p_idx
                p_idx += 1
            else:
                pass
        return frame_info, index_info

    @staticmethod
    def get_stream_arg(filepath):
        """
        整段视频的数据（video和audio）
        :param filepath:
        :return:
        """
        #整段视频的数据（video和audio）
        vsinfor = 'ffprobe -v quiet -print_format json -show_format -show_streams %s' % filepath
        print(vsinfor)
        pi = os.popen(vsinfor, 'r', 1).read()
        print(type(pi))
        print(pi)
        json_dict = json.loads(pi)
        # print('轨道数 %s'%len(json_dict['streams']))#有多少个轨道u
        video_result = dict()
        for idx, i in enumerate(json_dict['streams']):
            index = i['index']+1#编号
            codec_type = i['codec_type']#编码类型
            duration = i['duration']#视频的时长
            bit_rate = i['bit_rate']#码率
            r_frame_rate = i['r_frame_rate']#帧率
            nb_frames = i['nb_frames']#帧数
            if i.get('codec_type') == 'video':
                if 'width' in i.keys() and 'height' in i.keys() and 'has_b_frames'in i.keys():
                    fbl = '%s * %s' % (i['width'], i['height'])#分辨率
                    b_frames = i['has_b_frames']#含B帧的信息
                video_result['vedio'] = {
                    'index': index,
                    'codec_type': codec_type,
                    'duration':duration,
                    'fbl':fbl,
                    'bit_rate':bit_rate,
                    'b_frames':b_frames,
                    'r_frame_rate':r_frame_rate,
                    'nb_frames':nb_frames,
                }
            else:
                video_result['audio'] = {
                    'index': index,
                    'codec_type': codec_type,
                    'duration':duration,
                    'nb_frames':nb_frames,
                }
        return video_result



class Report:
    # 通用主题
    theme_js = """(function (root, factory) {
    if (typeof define === 'function' && define.amd) {
        // AMD. Register as an anonymous module.
        define(['exports', 'echarts'], factory);
    } else if (typeof exports === 'object' && typeof exports.nodeName !== 'string') {
        // CommonJS
        factory(exports, require('echarts'));
    } else {
        // Browser globals
        factory({}, root.echarts);
    }
}(this, function (exports, echarts) {
    var log = function (msg) {
        if (typeof console !== 'undefined') {
            console && console.error && console.error(msg);
        }
    };
    if (!echarts) {
        log('ECharts is not Loaded');
        return;
    }

    var colorPalette = [
        '#2ec7c9','#b6a2de','#5ab1ef','#ffb980','#d87a80',
        '#8d98b3','#e5cf0d','#97b552','#95706d','#dc69aa',
        '#07a2a4','#9a7fd1','#588dd5','#f5994e','#c05050',
        '#59678c','#c9ab00','#7eb00a','#6f5553','#c14089'
    ];


    var theme = {
        color: colorPalette,

        title: {
            textStyle: {
                fontWeight: 'normal',
                color: '#008acd'
            }
        },

        visualMap: {
            itemWidth: 15,
            color: ['#5ab1ef','#e0ffff']
        },

        toolbox: {
            iconStyle: {
                normal: {
                    borderColor: colorPalette[0]
                }
            }
        },

        tooltip: {
            backgroundColor: 'rgba(50,50,50,0.5)',
            axisPointer : {
                type : 'line',
                lineStyle : {
                    color: '#008acd'
                },
                crossStyle: {
                    color: '#008acd'
                },
                shadowStyle : {
                    color: 'rgba(200,200,200,0.2)'
                }
            }
        },

        dataZoom: {
            dataBackgroundColor: '#efefff',
            fillerColor: 'rgba(182,162,222,0.2)',
            handleColor: '#008acd'
        },

        grid: {
            borderColor: '#eee'
        },

        categoryAxis: {
            axisLine: {
                lineStyle: {
                    color: '#008acd'
                }
            },
            splitLine: {
                lineStyle: {
                    color: ['#eee']
                }
            }
        },

        valueAxis: {
            axisLine: {
                lineStyle: {
                    color: '#008acd'
                }
            },
            splitArea : {
                show : true,
                areaStyle : {
                    color: ['rgba(250,250,250,0.1)','rgba(200,200,200,0.1)']
                }
            },
            splitLine: {
                lineStyle: {
                    color: ['#eee']
                }
            }
        },

        timeline : {
            lineStyle : {
                color : '#008acd'
            },
            controlStyle : {
                normal : { color : '#008acd'},
                emphasis : { color : '#008acd'}
            },
            symbol : 'emptyCircle',
            symbolSize : 3
        },

        line: {
            smooth : true,
            symbol: 'emptyCircle',
            symbolSize: 3
        },

        candlestick: {
            itemStyle: {
                normal: {
                    color: '#d87a80',
                    color0: '#2ec7c9',
                    lineStyle: {
                        color: '#d87a80',
                        color0: '#2ec7c9'
                    }
                }
            }
        },

        scatter: {
            symbol: 'circle',
            symbolSize: 4
        },

        map: {
            label: {
                normal: {
                    textStyle: {
                        color: '#d87a80'
                    }
                }
            },
            itemStyle: {
                normal: {
                    borderColor: '#eee',
                    areaColor: '#ddd'
                },
                emphasis: {
                    areaColor: '#fe994e'
                }
            }
        },

        graph: {
            color: colorPalette
        },

        gauge : {
            axisLine: {
                lineStyle: {
                    color: [[0.2, '#2ec7c9'],[0.8, '#5ab1ef'],[1, '#d87a80']],
                    width: 10
                }
            },
            axisTick: {
                splitNumber: 10,
                length :15,
                lineStyle: {
                    color: 'auto'
                }
            },
            splitLine: {
                length :22,
                lineStyle: {
                    color: 'auto'
                }
            },
            pointer : {
                width : 5
            }
        }
    };

    echarts.registerTheme('macarons', theme);
}));"""
    # echarts 页面动态渲染
    info_frame_js = """$(document).ready(function() {
	frame_num = [];
	frame_duration = [];
	frame_bytes = [];
	frame_type = [];
	audio_A = [];
	audio_B = [];
	//格式化视频音频信息
	for(var i = 0; i<frame_info.length; i++){
		frame_num.push(i);
		if(frame_info[i]['media_type'] == 'video'){
			//当前帧的持续时间 = 下一帧的播放时刻 - 当前帧的播放时刻
			frame_duration.push(Math.round(frame_info[i]['pkt_duration_time'] * 1000, 2));
			frame_bytes.push(Math.round(frame_info[i]['pkt_size'], 4));
			frame_type.push(frame_info[i]['pict_type']);
			audio_A.push(null);
			audio_B.push(null);
		}
		else if(frame_info[i]['media_type'] == 'audio'){
			frame_duration.push(null);
			frame_bytes.push(null);
			frame_type.push(null);
			if(frame_info[i]['stream_index'] == 1){
				audio_A.push(frame_info[i]['pkt_size']);
				audio_B.push(null);
			}else if (frame_info[i]['stream_index'] == 2){
				audio_A.push(null);
				audio_B.push(frame_info[i]['pkt_size']);
			}
		}
	}
	//提示框获取指定坐标系数据
	function getAxisVal(params, num){
		num -= 1;
		for(var i = 0; i < params.length; i++){
			if(params[i]['componentIndex'] == num){
				return params[i]
			}
		}
		return false
	}
	//提示框格式化
	function fmtTips(params){
		args = params;
		//a-b 升序，b-a 降序
		args.sort(function(a, b){ return a['componentIndex'] - b['componentIndex']});//数据按坐标系从上到下的顺序排序
		res = '';
		img_name = '';
		idx = args[0]['name'];
		//console.log(frame_type);
		if (frame_info[idx]['media_type'] == 'video'){
			//视频信息格式化步骤
			name_1 = args[0]['seriesName'];
			value_1 = args[0]['value'];
			name_2 = args[1]['seriesName'];
			value_2 = args[1]['value'];
			play_t = frame_info[idx]['pkt_pts_time'];
			play_duration = frame_info[idx]['pkt_duration_time'];
			info = '帧详细参数：<br/>' + name_1 + '：'+ value_1 + '(ms)<br/>' + name_2 + '：'+ value_2 + '(byte)<br/>' + '播放时刻：' + play_t + '(s)<br/>' + '播放时长：' + play_duration +  '(s)<br/>';
			if (frame_type[idx] == 'I'){
				res = '<h3>I帧</h3><br/>';
				img_name = index_info[idx];
			}else if (frame_type[idx] == 'P'){
				res = '<h3>P帧</h3><br/>';
				img_name = index_info[idx];
			}else {
				res = '<h3>B帧</h3><br/>';
				return res + "frame_idx："+ idx + '<br/>' + info
			}
			return res + "<img style='width:350px;height:250px;' src='img/"+ img_name +"'/><br/>frame_idx："+ idx + '<br/>' + info
		}else if(frame_info[idx]['media_type'] == 'audio'){
			console.log(params);
			axis_3 = getAxisVal(args, 3);
			if(axis_3){
				name = axis_3['seriesName'];
				value = axis_3['value'];
				if(value != undefined){
					nb_samples = frame_info[idx]['nb_samples'];
					return name + '：'+ value + '<br/>采样率：' + nb_samples;
				}
				
			}
			axis_4 = getAxisVal(args, 4);
			if(axis_4){
				name = axis_4['seriesName'];
				value = axis_4['value'];
				if(value != undefined){
					nb_samples = frame_info[idx]['nb_samples'];
					return name + '：'+ value + '<br/>采样率：' + nb_samples;
				}
			}
			return ''
		}
	}
	//数据点大小格式化
	function fmtSymbolSize(point_value, params){
		//console.log(point_value);//y轴刻度值
		//console.log(params);//该点对应数据块信息，后续根据对应的帧号判断帧类型并在坐标系中标识出来
		frame_symbol_size = {'I': 12, 'P': 6, 'B': 2};
		return frame_symbol_size[frame_type[params['dataIndex']]]
	}
	//列表数据格式化
	function fmtSeries(axisIdx, name, symbolSize, data){
		base_series = {'type': 'line', 'xAxisIndex': axisIdx, 'yAxisIndex': axisIdx, 'animation': false, 'connectNulls': true, 'showAllSymbol': true};
		base_series['name'] = name;
		base_series['symbolSize'] = symbolSize;
		base_series['data'] = data;
		return base_series
	}
	//X轴数据格式化
	function fmtXaxis(axisIdx, data){
		return {'gridIndex': axisIdx, 'type': 'category', 'boundaryGap': false, 'axisLine': {'onZero': true}, 'data': data}
	}
	//Y轴数据格式化
	function fmtYaxis(axisIdx, name){
		return {'gridIndex': axisIdx, 'type': 'value', 'name': name}
	}
	axis_title = {'subtext': '数据来QAzone', 'x': 'left'};
	axis_tooltip = {'trigger': 'axis','formatter': fmtTips};
	axis_legend = {'data':['播放时长','帧大小','音轨A大小','音轨B大小'], 'x': 'center'};
	axis_toolbox = {'feature': {'restore': {}, 'saveAsImage': {}}};
	axis_axisPointer = {'link': {'xAxisIndex': 'all'}};
	axis_dataZoom = [
		{'type': 'slider', 'start': 0, 'end': 30, 'xAxisIndex': [0, 1, 2, 3]}, 
		{'type': 'inside', 'start': 0, 'end': 30, 'xAxisIndex': [0, 1, 2, 3]}
	];
	axis_grid = [
		{'left': 50, 'right': 50, 'top': '10%', 'height': '15%'},//每个坐标系间隔10%
		{'left': 50, 'right': 50, 'top': '35%', 'height': '15%'},
		{'left': 50, 'right': 50, 'top': '60%', 'height': '10%'},
		{'left': 50, 'right': 50, 'top': '80%', 'height': '10%'}
	];
	axis_xAxis = [fmtXaxis(0, frame_num), fmtXaxis(1, frame_num), fmtXaxis(2, frame_num), fmtXaxis(3, frame_num)];
	axis_yAxis = [fmtYaxis(0, '播放时长(ms)'),fmtYaxis(1, '帧大小(byte)'),fmtYaxis(2, '音轨A大小'),fmtYaxis(3, '音轨B大小')];
	axis_series = [
		fmtSeries(0, '播放时长', fmtSymbolSize, frame_duration),
		fmtSeries(1, '帧大小', fmtSymbolSize, frame_bytes),
		fmtSeries(2, '音轨A大小', 2, audio_A),
		fmtSeries(3, '音轨B大小', 2, audio_B)
	];
	option = {
		'title': axis_title,
		'tooltip': axis_tooltip,
		'legend': axis_legend,
		'toolbox': axis_toolbox,
		'axisPointer': axis_axisPointer,
		'dataZoom': axis_dataZoom,
		'grid': axis_grid,
		'xAxis': axis_xAxis,
		'yAxis': axis_yAxis,
		'series': axis_series
	};
	// 基于准备好的dom，初始化echarts实例
	var LineChart = echarts.init(document.getElementById('line'), 'macarons');
	// 使用刚指定的配置项和数据显示图表。
	LineChart.setOption(option);
});

"""
    # html页面
    info_html = """<!DOCTYPE html>
<html>
	<head>
		<meta charset="utf-8">
		<title>VideoInfo</title>
		<!-- 加载jquery -->
		<script src="https://cdn.bootcss.com/jquery/3.3.1/jquery.js"></script>
		<!-- 加载bootstrap -->
		<link href="https://cdn.bootcss.com/twitter-bootstrap/4.2.1/css/bootstrap.min.css" rel="stylesheet">
		<script src="https://cdn.bootcss.com/twitter-bootstrap/4.2.1/js/bootstrap.min.js"></script>
		<!-- 加载echarts及echarts主题-->
		<script src="https://cdn.bootcss.com/echarts/4.2.0-rc.2/echarts.js"></script>
		<script src="theme.js"></script>
		<!-- 加载自定义js -->
		<script src="data.js"></script>
	</head>
	<body>
		<div class="container">
			<h1>视频帧详情展示</h1>
			<pre>1, 播放时长，播放一帧需要的时长，可以大体看出每帧播放的顺滑程度。<br/>2，帧大小，帧的字节容量，辅助参考值。<br/>3，音轨，视频文件的音频轨道信息。<br/>ps:建议应用于时长在一分钟内的视频</pre>
			<div class="row clearfix">
				<div class="col-md-12 column">
					<div id="line" style="height:750px;"></div>
				</div>
			</div>
		</div>
		<script src="frame.js"></script>
	</body>
</html>"""
    cmp_frame_js =  """
$(document).ready(function() {
	// 指定雷达图的配置项
	var radar_option = {
		title : radar_title,
		tooltip : {},
		legend: {
			orient : 'horizontal',
			data: product,
		},
		toolbox: {
			feature : {
				mark : {show: true},
				restore : {show: true},
				saveAsImage : {show: true}
			}
		},
		radar : {
			splitNumber: 5,
			indicator: radar_indicator,
		},
		calculable : true,
		series : [
			{
				name: 'radar_show',
				type: 'radar',
				data : radar_data,
			}
		]
	};
	
	//指定柱状图的配置项
	var bar_option = {
		title : {},
		color: ['#3398DB'],
		tooltip : {
			trigger: 'axis',
			axisPointer : {            // 坐标轴指示器，坐标轴触发有效
				type : 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
			}
		},
		toolbox: {
			feature:{
				magicType: {show: true, type: ['line', 'bar']}
			}
		},
		xAxis : [
			{
				type : 'category',
				data : product,
				axisTick: {
					alignWithLabel: true,
				},
				axisLabel: {
					interval: 0,
					formatter: function(str){
						if(str.length > 3){
							return str.slice(0,3)+'…'
						}
						return str
					}
				},
			}
		],
		yAxis : [
			{
				type : 'value'
			}
		],
		series : [
			{
				name:'',
				type:'bar',
				barWidth: '50%',
				data: []
			}
		]
	};
	// 基于准备好的dom，初始化echarts实例
	//var RadarChart = echarts.init(document.getElementById('radar'), 'macarons');
    var RadarChart = echarts.init(document.getElementById('radar'));
	// 使用刚指定的配置项和数据显示图表。
	RadarChart.setOption(radar_option);
	
	//动态配置柱状图阵列
	var div_list = document.getElementsByName('report_bar');//获取所有柱状图列表	
	for (var i =1; i <=div_list.length; i++) {
		var bar_id = 'bar'+i;
		if(i <= bar_settings.length){
			console.log("FIND BAR: %s TO DISPLAY", bar_id);
			var div = div_list[i-1];
			div.style.display = 'block';
			var BarDiv = echarts.init(div, 'macarons');
			bar_option['title'] = bar_settings[i-1]['title']
			bar_option['series'][0]['data'] = bar_settings[i-1]['data']
			bar_option['series'][0]['name'] = bar_settings[i-1]['name']
			BarDiv.setOption(bar_option);
			console.log("%s DISPLAY OVER", bar_id);
		}else{
			break;
		}
	}

});"""
    cmp_html = """
<!DOCTYPE html>
<html>
	<head>
		<meta charset="utf-8">
		<title>VideoCompare</title>
		<link href="https://cdn.staticfile.org/twitter-bootstrap/3.3.7/css/bootstrap.min.css" rel="stylesheet">
		<script src="https://cdn.staticfile.org/jquery/2.1.1/jquery.min.js"></script>
		<script src="https://cdn.staticfile.org/twitter-bootstrap/3.3.7/js/bootstrap.min.js"></script>
		<!-- 引入 echarts.js及echarts主题-->
		<script src="http://echarts.baidu.com/dist/echarts3/echarts.min.js"></script>
		<script src="http://echarts.baidu.com/asset/theme/macarons.js"></script>
		<!-- 引入 echarts.js -->
		<script src="data.js"></script>
		<script src="frame.js"></script>
	</head>
	<body>
		<div class="container">
			<div class="row clearfix">
				<div class="col-md-12 column">
					<div class="row clearfix">
						<div class="col-md-12 column">
							<div id="radar" style="height:500px;"></div>
						</div>
					</div>
					<!--以下div根据data.js文件中的bar_settings数据动态填充，详见report.js-->
					<!--初始栏位-->
					<div class="row clearfix">
						<div class="col-md-4 column">
							<div name="report_bar" id="bar1" style="height:300px;display:none"></div>
						</div>
						<div class="col-md-4 column">
							<div name="report_bar" id="bar2" style="height:300px;display:none"></div>
						</div>
						<div class="col-md-4 column">
							<div name="report_bar" id="bar3" style="height:300px;display:none"></div>
						</div>
					</div>
					<!--预留栏位1-->
					<div class="row clearfix">
						<div class="col-md-4 column">
							<div name="report_bar" id="bar4" style="height:300px;display:none"></div>
						</div>
						<div class="col-md-4 column">
							<div name="report_bar" id="bar5" style="height:300px;display:none"></div>
						</div>
						<div class="col-md-4 column">
							<div name="report_bar" id="bar6" style="height:300px;display:none"></div>
						</div>
					</div>
					<!--预留栏位2-->
					<div class="row clearfix">
						<div class="col-md-4 column">
							<div name="report_bar" id="bar7" style="height:300px;display:none"></div>
						</div>
						<div class="col-md-4 column">
							<div name="report_bar" id="bar8" style="height:300px;display:none"></div>
						</div>
						<div class="col-md-4 column">
							<div name="report_bar" id="bar9" style="height:300px;display:none"></div>
						</div>
					</div>
					<!--预留栏位，数据不足时可继续扩充-->
				</div>
			</div>
		</div>
	</body>
</html>"""
    """
      写入每一帧文件到HTML，数据与网页的接口
    """
    @staticmethod
    def echo_theme_js(target):
        d = os.path.join(target, 'theme.js')
        with open(d, 'w', encoding='utf-8') as f:
            f.write(Report.theme_js)

    @staticmethod
    def echo_info_frame_js(target):
        d = os.path.join(target, 'frame.js')
        with open(d, 'w', encoding='utf-8') as f:
            f.write(Report.info_frame_js)

    @staticmethod
    def echo_info_html(target):
        d = os.path.join(target, 'index.html')
        with open(d, 'w', encoding='utf-8') as f:
            f.write(Report.info_html)

    # 动态数据
    @staticmethod
    def echo_info_data(target, frame_info, index_info):
        d = os.path.join(target, 'data.js')
        with open(d, 'w', encoding='utf-8') as f:
            f.write('frame_info = %s;\n' % json.dumps(frame_info))
            f.write('index_info = %s;\n;' % json.dumps(index_info))
    """
     写入整个视频文件到HTML，数据与网页的接口
   """
    @staticmethod
    def echo_cmp_frame_js(target):
        d = os.path.join(target, 'frame.js')
        with open(d, 'w', encoding='utf-8') as f:
            f.write(Report.cmp_frame_js)

    @staticmethod
    def echo_cmp_html(target):
        d = os.path.join(target, 'index.html')
        with open(d, 'w', encoding='utf-8') as f:
            f.write(Report.cmp_html)

    @staticmethod
    def echo_cmp_data(target, product, title, indicator, radar_data, bar_data):
        d = os.path.join(target, 'data.js')
        with open(d, 'w', encoding='utf-8') as f:
            f.write('product = %s;\n' % json.dumps(product))
            f.write('radar_title = %s;\n' % json.dumps(title))
            f.write('radar_indicator = %s;\n' % json.dumps(indicator))
            f.write('radar_data = %s;\n' % json.dumps(radar_data))
            f.write('bar_settings = %s;\n' % json.dumps(bar_data))

