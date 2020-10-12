import json


def get_cwnd():
    cwnd = []
    s = '''{
	"start":	{
		"connected":	[{
				"socket":	17,
				"local_host":	"10.0.0.1",
				"local_port":	47790,
				"remote_host":	"10.0.0.2",
				"remote_port":	5201
			}],
		"version":	"iperf 3.1.3",
		"system_info":	"Linux ubuntu-xenial 4.15.0-117-generic #118-Ubuntu SMP Fri Sep 4 20:02:41 UTC 2020 x86_64",
		"timestamp":	{
			"time":	"Tue, 22 Sep 2020 11:25:03 GMT",
			"timesecs":	1600773903
		},
		"connecting_to":	{
			"host":	"10.0.0.2",
			"port":	5201
		},
		"cookie":	"ubuntu-xenial.1600773902.821173.19da",
		"tcp_mss_default":	1448,
		"test_start":	{
			"protocol":	"TCP",
			"num_streams":	1,
			"blksize":	131072,
			"omit":	0,
			"duration":	40,
			"bytes":	0,
			"blocks":	0,
			"reverse":	0
		}
	},
	"intervals":	[{
			"streams":	[{
					"socket":	17,
					"start":	0,
					"end":	1.000073,
					"seconds":	1.000073,
					"bytes":	628432,
					"bits_per_second":	5027089.243249,
					"retransmits":	0,
					"snd_cwnd":	14480,
					"rtt":	7297,
					"omitted":	false
				}],
			"sum":	{
				"start":	0,
				"end":	1.000073,
				"seconds":	1.000073,
				"bytes":	628432,
				"bits_per_second":	5027089.243249,
				"retransmits":	0,
				"omitted":	false
			}
		}, {
			"streams":	[{
					"socket":	17,
					"start":	1.000073,
					"end":	2.000129,
					"seconds":	1.000056,
					"bytes":	599472,
					"bits_per_second":	4795507.315561,
					"retransmits":	0,
					"snd_cwnd":	14480,
					"rtt":	7245,
					"omitted":	false
				}],
			"sum":	{
				"start":	1.000073,
				"end":	2.000129,
				"seconds":	1.000056,
				"bytes":	599472,
				"bits_per_second":	4795507.315561,
				"retransmits":	0,
				"omitted":	false
			}
		}, {
			"streams":	[{
					"socket":	17,
					"start":	2.000129,
					"end":	3.000128,
					"seconds":	0.999999,
					"bytes":	596576,
					"bits_per_second":	4772612.551518,
					"retransmits":	0,
					"snd_cwnd":	14480,
					"rtt":	7286,
					"omitted":	false
				}],
			"sum":	{
				"start":	2.000129,
				"end":	3.000128,
				"seconds":	0.999999,
				"bytes":	596576,
				"bits_per_second":	4772612.551518,
				"retransmits":	0,
				"omitted":	false
			}
		}, {
			"streams":	[{
					"socket":	17,
					"start":	3.000128,
					"end":	4.000102,
					"seconds":	0.999974,
					"bytes":	596576,
					"bits_per_second":	4772732.031971,
					"retransmits":	0,
					"snd_cwnd":	14480,
					"rtt":	7275,
					"omitted":	false
				}],
			"sum":	{
				"start":	3.000128,
				"end":	4.000102,
				"seconds":	0.999974,
				"bytes":	596576,
				"bits_per_second":	4772732.031971,
				"retransmits":	0,
				"omitted":	false
			}
		}, {
			"streams":	[{
					"socket":	17,
					"start":	4.000102,
					"end":	5.000040,
					"seconds":	0.999938,
					"bytes":	598024,
					"bits_per_second":	4784488.584852,
					"retransmits":	0,
					"snd_cwnd":	14480,
					"rtt":	7277,
					"omitted":	false
				}],
			"sum":	{
				"start":	4.000102,
				"end":	5.000040,
				"seconds":	0.999938,
				"bytes":	598024,
				"bits_per_second":	4784488.584852,
				"retransmits":	0,
				"omitted":	false
			}
		}, {
			"streams":	[{
					"socket":	17,
					"start":	5.000040,
					"end":	6.001091,
					"seconds":	1.001051,
					"bytes":	592232,
					"bits_per_second":	4732881.981956,
					"retransmits":	0,
					"snd_cwnd":	14480,
					"rtt":	6849,
					"omitted":	false
				}],
			"sum":	{
				"start":	5.000040,
				"end":	6.001091,
				"seconds":	1.001051,
				"bytes":	592232,
				"bits_per_second":	4732881.981956,
				"retransmits":	0,
				"omitted":	false
			}
		}, {
			"streams":	[{
					"socket":	17,
					"start":	6.001091,
					"end":	7.001986,
					"seconds":	1.000895,
					"bytes":	577752,
					"bits_per_second":	4617882.887007,
					"retransmits":	0,
					"snd_cwnd":	14480,
					"rtt":	6942,
					"omitted":	false
				}],
			"sum":	{
				"start":	6.001091,
				"end":	7.001986,
				"seconds":	1.000895,
				"bytes":	577752,
				"bits_per_second":	4617882.887007,
				"retransmits":	0,
				"omitted":	false
			}
		}, {
			"streams":	[{
					"socket":	17,
					"start":	7.001986,
					"end":	8.000209,
					"seconds":	0.998223,
					"bytes":	584992,
					"bits_per_second":	4688266.739023,
					"retransmits":	0,
					"snd_cwnd":	14480,
					"rtt":	6420,
					"omitted":	false
				}],
			"sum":	{
				"start":	7.001986,
				"end":	8.000209,
				"seconds":	0.998223,
				"bytes":	584992,
				"bits_per_second":	4688266.739023,
				"retransmits":	0,
				"omitted":	false
			}
		}, {
			"streams":	[{
					"socket":	17,
					"start":	8.000209,
					"end":	9.001208,
					"seconds":	1.000999,
					"bytes":	587888,
					"bits_per_second":	4698410.410880,
					"retransmits":	0,
					"snd_cwnd":	14480,
					"rtt":	7134,
					"omitted":	false
				}],
			"sum":	{
				"start":	8.000209,
				"end":	9.001208,
				"seconds":	1.000999,
				"bytes":	587888,
				"bits_per_second":	4698410.410880,
				"retransmits":	0,
				"omitted":	false
			}
		}, {
			"streams":	[{
					"socket":	17,
					"start":	9.001208,
					"end":	10.000806,
					"seconds":	0.999598,
					"bytes":	582096,
					"bits_per_second":	4658640.651133,
					"retransmits":	0,
					"snd_cwnd":	14480,
					"rtt":	6966,
					"omitted":	false
				}],
			"sum":	{
				"start":	9.001208,
				"end":	10.000806,
				"seconds":	0.999598,
				"bytes":	582096,
				"bits_per_second":	4658640.651133,
				"retransmits":	0,
				"omitted":	false
			}
		}, {
			"streams":	[{
					"socket":	17,
					"start":	10.000806,
					"end":	11.001118,
					"seconds":	1.000312,
					"bytes":	584992,
					"bits_per_second":	4678475.894832,
					"retransmits":	0,
					"snd_cwnd":	14480,
					"rtt":	6816,
					"omitted":	false
				}],
			"sum":	{
				"start":	10.000806,
				"end":	11.001118,
				"seconds":	1.000312,
				"bytes":	584992,
				"bits_per_second":	4678475.894832,
				"retransmits":	0,
				"omitted":	false
			}
		}, {
			"streams":	[{
					"socket":	17,
					"start":	11.001118,
					"end":	12.002619,
					"seconds":	1.001501,
					"bytes":	584992,
					"bits_per_second":	4672922.667587,
					"retransmits":	0,
					"snd_cwnd":	14480,
					"rtt":	7224,
					"omitted":	false
				}],
			"sum":	{
				"start":	11.001118,
				"end":	12.002619,
				"seconds":	1.001501,
				"bytes":	584992,
				"bits_per_second":	4672922.667587,
				"retransmits":	0,
				"omitted":	false
			}
		}, {
			"streams":	[{
					"socket":	17,
					"start":	12.002619,
					"end":	13.003654,
					"seconds":	1.001035,
					"bytes":	582096,
					"bits_per_second":	4651953.344346,
					"retransmits":	0,
					"snd_cwnd":	14480,
					"rtt":	7116,
					"omitted":	false
				}],
			"sum":	{
				"start":	12.002619,
				"end":	13.003654,
				"seconds":	1.001035,
				"bytes":	582096,
				"bits_per_second":	4651953.344346,
				"retransmits":	0,
				"omitted":	false
			}
		}, {
			"streams":	[{
					"socket":	17,
					"start":	13.003654,
					"end":	14.003026,
					"seconds":	0.999372,
					"bytes":	582096,
					"bits_per_second":	4659694.262543,
					"retransmits":	0,
					"snd_cwnd":	14480,
					"rtt":	7084,
					"omitted":	false
				}],
			"sum":	{
				"start":	13.003654,
				"end":	14.003026,
				"seconds":	0.999372,
				"bytes":	582096,
				"bits_per_second":	4659694.262543,
				"retransmits":	0,
				"omitted":	false
			}
		}, {
			"streams":	[{
					"socket":	17,
					"start":	14.003026,
					"end":	15.000900,
					"seconds":	0.997874,
					"bytes":	584992,
					"bits_per_second":	4689906.640543,
					"retransmits":	0,
					"snd_cwnd":	14480,
					"rtt":	7493,
					"omitted":	false
				}],
			"sum":	{
				"start":	14.003026,
				"end":	15.000900,
				"seconds":	0.997874,
				"bytes":	584992,
				"bits_per_second":	4689906.640543,
				"retransmits":	0,
				"omitted":	false
			}
		}, {
			"streams":	[{
					"socket":	17,
					"start":	15.000900,
					"end":	16.003157,
					"seconds":	1.002257,
					"bytes":	590784,
					"bits_per_second":	4715628.314361,
					"retransmits":	0,
					"snd_cwnd":	14480,
					"rtt":	7175,
					"omitted":	false
				}],
			"sum":	{
				"start":	15.000900,
				"end":	16.003157,
				"seconds":	1.002257,
				"bytes":	590784,
				"bits_per_second":	4715628.314361,
				"retransmits":	0,
				"omitted":	false
			}
		}, {
			"streams":	[{
					"socket":	17,
					"start":	16.003157,
					"end":	17.001054,
					"seconds":	0.997897,
					"bytes":	580648,
					"bits_per_second":	4654973.830245,
					"retransmits":	0,
					"snd_cwnd":	14480,
					"rtt":	7180,
					"omitted":	false
				}],
			"sum":	{
				"start":	16.003157,
				"end":	17.001054,
				"seconds":	0.997897,
				"bytes":	580648,
				"bits_per_second":	4654973.830245,
				"retransmits":	0,
				"omitted":	false
			}
		}, {
			"streams":	[{
					"socket":	17,
					"start":	17.001054,
					"end":	18.000554,
					"seconds":	0.999500,
					"bytes":	584992,
					"bits_per_second":	4682276.968800,
					"retransmits":	0,
					"snd_cwnd":	14480,
					"rtt":	7248,
					"omitted":	false
				}],
			"sum":	{
				"start":	17.001054,
				"end":	18.000554,
				"seconds":	0.999500,
				"bytes":	584992,
				"bits_per_second":	4682276.968800,
				"retransmits":	0,
				"omitted":	false
			}
		}, {
			"streams":	[{
					"socket":	17,
					"start":	18.000554,
					"end":	19.001027,
					"seconds":	1.000473,
					"bytes":	583544,
					"bits_per_second":	4666144.808699,
					"retransmits":	0,
					"snd_cwnd":	14480,
					"rtt":	6938,
					"omitted":	false
				}],
			"sum":	{
				"start":	18.000554,
				"end":	19.001027,
				"seconds":	1.000473,
				"bytes":	583544,
				"bits_per_second":	4666144.808699,
				"retransmits":	0,
				"omitted":	false
			}
		}, {
			"streams":	[{
					"socket":	17,
					"start":	19.001027,
					"end":	20.000318,
					"seconds":	0.999291,
					"bytes":	584992,
					"bits_per_second":	4683256.695260,
					"retransmits":	0,
					"snd_cwnd":	14480,
					"rtt":	7136,
					"omitted":	false
				}],
			"sum":	{
				"start":	19.001027,
				"end":	20.000318,
				"seconds":	0.999291,
				"bytes":	584992,
				"bits_per_second":	4683256.695260,
				"retransmits":	0,
				"omitted":	false
			}
		}, {
			"streams":	[{
					"socket":	17,
					"start":	20.000318,
					"end":	21.001893,
					"seconds":	1.001575,
					"bytes":	584992,
					"bits_per_second":	4672576.723744,
					"retransmits":	0,
					"snd_cwnd":	14480,
					"rtt":	6867,
					"omitted":	false
				}],
			"sum":	{
				"start":	20.000318,
				"end":	21.001893,
				"seconds":	1.001575,
				"bytes":	584992,
				"bits_per_second":	4672576.723744,
				"retransmits":	0,
				"omitted":	false
			}
		}, {
			"streams":	[{
					"socket":	17,
					"start":	21.001893,
					"end":	22.003294,
					"seconds":	1.001401,
					"bytes":	583544,
					"bits_per_second":	4661821.033148,
					"retransmits":	0,
					"snd_cwnd":	14480,
					"rtt":	6991,
					"omitted":	false
				}],
			"sum":	{
				"start":	21.001893,
				"end":	22.003294,
				"seconds":	1.001401,
				"bytes":	583544,
				"bits_per_second":	4661821.033148,
				"retransmits":	0,
				"omitted":	false
			}
		}, {
			"streams":	[{
					"socket":	17,
					"start":	22.003294,
					"end":	23.000598,
					"seconds":	0.997304,
					"bytes":	584992,
					"bits_per_second":	4692587.390603,
					"retransmits":	0,
					"snd_cwnd":	14480,
					"rtt":	7197,
					"omitted":	false
				}],
			"sum":	{
				"start":	22.003294,
				"end":	23.000598,
				"seconds":	0.997304,
				"bytes":	584992,
				"bits_per_second":	4692587.390603,
				"retransmits":	0,
				"omitted":	false
			}
		}, {
			"streams":	[{
					"socket":	17,
					"start":	23.000598,
					"end":	24.000416,
					"seconds":	0.999818,
					"bytes":	580648,
					"bits_per_second":	4646029.174852,
					"retransmits":	0,
					"snd_cwnd":	14480,
					"rtt":	6739,
					"omitted":	false
				}],
			"sum":	{
				"start":	23.000598,
				"end":	24.000416,
				"seconds":	0.999818,
				"bytes":	580648,
				"bits_per_second":	4646029.174852,
				"retransmits":	0,
				"omitted":	false
			}
		}, {
			"streams":	[{
					"socket":	17,
					"start":	24.000416,
					"end":	25.001893,
					"seconds":	1.001477,
					"bytes":	586440,
					"bits_per_second":	4684600.830063,
					"retransmits":	0,
					"snd_cwnd":	14480,
					"rtt":	6968,
					"omitted":	false
				}],
			"sum":	{
				"start":	24.000416,
				"end":	25.001893,
				"seconds":	1.001477,
				"bytes":	586440,
				"bits_per_second":	4684600.830063,
				"retransmits":	0,
				"omitted":	false
			}
		}, {
			"streams":	[{
					"socket":	17,
					"start":	25.001893,
					"end":	26.001337,
					"seconds":	0.999444,
					"bytes":	584992,
					"bits_per_second":	4682539.455069,
					"retransmits":	0,
					"snd_cwnd":	14480,
					"rtt":	6827,
					"omitted":	false
				}],
			"sum":	{
				"start":	25.001893,
				"end":	26.001337,
				"seconds":	0.999444,
				"bytes":	584992,
				"bits_per_second":	4682539.455069,
				"retransmits":	0,
				"omitted":	false
			}
		}, {
			"streams":	[{
					"socket":	17,
					"start":	26.001337,
					"end":	27.000633,
					"seconds":	0.999296,
					"bytes":	584992,
					"bits_per_second":	4683233.230656,
					"retransmits":	0,
					"snd_cwnd":	14480,
					"rtt":	6966,
					"omitted":	false
				}],
			"sum":	{
				"start":	26.001337,
				"end":	27.000633,
				"seconds":	0.999296,
				"bytes":	584992,
				"bits_per_second":	4683233.230656,
				"retransmits":	0,
				"omitted":	false
			}
		}, {
			"streams":	[{
					"socket":	17,
					"start":	27.000633,
					"end":	28.000208,
					"seconds":	0.999575,
					"bytes":	586440,
					"bits_per_second":	4693514.095354,
					"retransmits":	0,
					"snd_cwnd":	14480,
					"rtt":	6856,
					"omitted":	false
				}],
			"sum":	{
				"start":	27.000633,
				"end":	28.000208,
				"seconds":	0.999575,
				"bytes":	586440,
				"bits_per_second":	4693514.095354,
				"retransmits":	0,
				"omitted":	false
			}
		}, {
			"streams":	[{
					"socket":	17,
					"start":	28.000208,
					"end":	29.003866,
					"seconds":	1.003658,
					"bytes":	586440,
					"bits_per_second":	4674421.816485,
					"retransmits":	0,
					"snd_cwnd":	14480,
					"rtt":	6711,
					"omitted":	false
				}],
			"sum":	{
				"start":	28.000208,
				"end":	29.003866,
				"seconds":	1.003658,
				"bytes":	586440,
				"bits_per_second":	4674421.816485,
				"retransmits":	0,
				"omitted":	false
			}
		}, {
			"streams":	[{
					"socket":	17,
					"start":	29.003866,
					"end":	30.000305,
					"seconds":	0.996439,
					"bytes":	582096,
					"bits_per_second":	4673408.988168,
					"retransmits":	0,
					"snd_cwnd":	14480,
					"rtt":	7158,
					"omitted":	false
				}],
			"sum":	{
				"start":	29.003866,
				"end":	30.000305,
				"seconds":	0.996439,
				"bytes":	582096,
				"bits_per_second":	4673408.988168,
				"retransmits":	0,
				"omitted":	false
			}
		}, {
			"streams":	[{
					"socket":	17,
					"start":	30.000305,
					"end":	31.000623,
					"seconds":	1.000318,
					"bytes":	598024,
					"bits_per_second":	4782672.009606,
					"retransmits":	0,
					"snd_cwnd":	21720,
					"rtt":	6569,
					"omitted":	false
				}],
			"sum":	{
				"start":	30.000305,
				"end":	31.000623,
				"seconds":	1.000318,
				"bytes":	598024,
				"bits_per_second":	4782672.009606,
				"retransmits":	0,
				"omitted":	false
			}
		}, {
			"streams":	[{
					"socket":	17,
					"start":	31.000623,
					"end":	32.002635,
					"seconds":	1.002012,
					"bytes":	589336,
					"bits_per_second":	4705221.027589,
					"retransmits":	0,
					"snd_cwnd":	21720,
					"rtt":	6785,
					"omitted":	false
				}],
			"sum":	{
				"start":	31.000623,
				"end":	32.002635,
				"seconds":	1.002012,
				"bytes":	589336,
				"bits_per_second":	4705221.027589,
				"retransmits":	0,
				"omitted":	false
			}
		}, {
			"streams":	[{
					"socket":	17,
					"start":	32.002635,
					"end":	33.003101,
					"seconds":	1.000466,
					"bytes":	584992,
					"bits_per_second":	4677755.659158,
					"retransmits":	0,
					"snd_cwnd":	21720,
					"rtt":	7016,
					"omitted":	false
				}],
			"sum":	{
				"start":	32.002635,
				"end":	33.003101,
				"seconds":	1.000466,
				"bytes":	584992,
				"bits_per_second":	4677755.659158,
				"retransmits":	0,
				"omitted":	false
			}
		}, {
			"streams":	[{
					"socket":	17,
					"start":	33.003101,
					"end":	34.000695,
					"seconds":	0.997594,
					"bytes":	587888,
					"bits_per_second":	4714447.527902,
					"retransmits":	0,
					"snd_cwnd":	21720,
					"rtt":	6930,
					"omitted":	false
				}],
			"sum":	{
				"start":	33.003101,
				"end":	34.000695,
				"seconds":	0.997594,
				"bytes":	587888,
				"bits_per_second":	4714447.527902,
				"retransmits":	0,
				"omitted":	false
			}
		}, {
			"streams":	[{
					"socket":	17,
					"start":	34.000695,
					"end":	35.003572,
					"seconds":	1.002877,
					"bytes":	583544,
					"bits_per_second":	4654959.694950,
					"retransmits":	0,
					"snd_cwnd":	21720,
					"rtt":	7428,
					"omitted":	false
				}],
			"sum":	{
				"start":	34.000695,
				"end":	35.003572,
				"seconds":	1.002877,
				"bytes":	583544,
				"bits_per_second":	4654959.694950,
				"retransmits":	0,
				"omitted":	false
			}
		}, {
			"streams":	[{
					"socket":	17,
					"start":	35.003572,
					"end":	36.001353,
					"seconds":	0.997781,
					"bytes":	587888,
					"bits_per_second":	4713563.216322,
					"retransmits":	0,
					"snd_cwnd":	21720,
					"rtt":	6602,
					"omitted":	false
				}],
			"sum":	{
				"start":	35.003572,
				"end":	36.001353,
				"seconds":	0.997781,
				"bytes":	587888,
				"bits_per_second":	4713563.216322,
				"retransmits":	0,
				"omitted":	false
			}
		}, {
			"streams":	[{
					"socket":	17,
					"start":	36.001353,
					"end":	37.000169,
					"seconds":	0.998816,
					"bytes":	576304,
					"bits_per_second":	4615897.160680,
					"retransmits":	0,
					"snd_cwnd":	21720,
					"rtt":	6190,
					"omitted":	false
				}],
			"sum":	{
				"start":	36.001353,
				"end":	37.000169,
				"seconds":	0.998816,
				"bytes":	576304,
				"bits_per_second":	4615897.160680,
				"retransmits":	0,
				"omitted":	false
			}
		}, {
			"streams":	[{
					"socket":	17,
					"start":	37.000169,
					"end":	38.001140,
					"seconds":	1.000971,
					"bytes":	582096,
					"bits_per_second":	4652250.298025,
					"retransmits":	0,
					"snd_cwnd":	21720,
					"rtt":	6991,
					"omitted":	false
				}],
			"sum":	{
				"start":	37.000169,
				"end":	38.001140,
				"seconds":	1.000971,
				"bytes":	582096,
				"bits_per_second":	4652250.298025,
				"retransmits":	0,
				"omitted":	false
			}
		}, {
			"streams":	[{
					"socket":	17,
					"start":	38.001140,
					"end":	39.001156,
					"seconds":	1.000016,
					"bytes":	584992,
					"bits_per_second":	4679861.243687,
					"retransmits":	0,
					"snd_cwnd":	21720,
					"rtt":	7440,
					"omitted":	false
				}],
			"sum":	{
				"start":	38.001140,
				"end":	39.001156,
				"seconds":	1.000016,
				"bytes":	584992,
				"bits_per_second":	4679861.243687,
				"retransmits":	0,
				"omitted":	false
			}
		}, {
			"streams":	[{
					"socket":	17,
					"start":	39.001156,
					"end":	40.000561,
					"seconds":	0.999405,
					"bytes":	589336,
					"bits_per_second":	4717495.347390,
					"retransmits":	0,
					"snd_cwnd":	21720,
					"rtt":	6875,
					"omitted":	false
				}],
			"sum":	{
				"start":	39.001156,
				"end":	40.000561,
				"seconds":	0.999405,
				"bytes":	589336,
				"bits_per_second":	4717495.347390,
				"retransmits":	0,
				"omitted":	false
			}
		}],
	"end":	{
		"streams":	[{
				"sender":	{
					"socket":	17,
					"start":	0,
					"end":	40.000561,
					"seconds":	40.000561,
					"bytes":	23498144,
					"bits_per_second":	4699562.888758,
					"retransmits":	0,
					"max_snd_cwnd":	21720,
					"max_rtt":	7493,
					"min_rtt":	6190,
					"mean_rtt":	7005
				},
				"receiver":	{
					"socket":	17,
					"start":	0,
					"end":	40.000561,
					"seconds":	40.000561,
					"bytes":	23460496,
					"bits_per_second":	4692033.394359
				}
			}],
		"sum_sent":	{
			"start":	0,
			"end":	40.000561,
			"seconds":	40.000561,
			"bytes":	23498144,
			"bits_per_second":	4699562.888758,
			"retransmits":	0
		},
		"sum_received":	{
			"start":	0,
			"end":	40.000561,
			"seconds":	40.000561,
			"bytes":	23460496,
			"bits_per_second":	4692033.394359
		},
		"cpu_utilization_percent":	{
			"host_total":	0.228769,
			"host_user":	0.141334,
			"host_system":	0.087432,
			"remote_total":	0.951897,
			"remote_user":	0.162337,
			"remote_system":	0.789555
		}
	}
}
'''
    iperf_json = json.loads(s)
    for stream_info in iperf_json['intervals']:
        stream_info = stream_info['streams'][0]
        cwnd.append(int(stream_info['snd_cwnd']))

    return cwnd

if __name__ == '__main__':
    get_cwnd()