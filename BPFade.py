# -*- coding: utf-8 -*-
import sys
import os

sys.path.append("../")
from blueprintBase import CBlueprintBase, make_Video
import outputDesc


class BPFade(CBlueprintBase):

    # input: https://videofactory.oss-cn-shanghai.aliyuncs.com/ios/video/mv_7.mp4
    # output:
    #           None: http://test-v.oss-cn-shanghai.aliyuncs.com/hypnos-blueprint/output-11104-484360.mp4
    #           in: http://test-v.oss-cn-shanghai.aliyuncs.com/hypnos-blueprint/output-11105-117533.mp4
    #           out: http://test-v.oss-cn-shanghai.aliyuncs.com/hypnos-blueprint/output-11114-108122.mp4
    # Value range for fade:
    #           None: Add fade-in and fade-out elements
    #           in: Add fade-in elements
    #           out: Add fade-out elements

    def __init__(self, user_element, width=720, height=1280, element_duration=None, action_configDict=None,
                 element_configDict=None, fadeinTime=1000, fadeoutTime=1000, fade=None, alpha_list=None):
        super(BPFade, self).__init__("Alpha")
        self._width = width
        self._height = height
        self._user_element = user_element
        self._element_duration = element_duration if element_duration else 3000
        self._action_configDict = action_configDict
        self._element_configDict = element_configDict
        self._element_type = self.get_elementType_fromValue(user_element)
        self._fadein_time = fadeinTime
        self._fadeout_time = fadeoutTime
        self._fade = fade

        if fade == 'in':
            self._times = [(0, self._fadein_time), (self._fadein_time, self._element_duration)]
            self._alpha_list = [(0.3, 1), (1, 1)] if not alpha_list else alpha_list
            self._action_num = 2
        elif fade == 'out':
            self._times = [(0, self._element_duration - self._fadeout_time),
                           (self._element_duration - self._fadeout_time, self._element_duration)]
            self._alpha_list = [(1, 1), (1, 0.3)] if not alpha_list else alpha_list
            self._action_num = 2
        else:
            self._times = [(0, self._fadein_time), (self._fadein_time, self._element_duration - self._fadeout_time),
                           (self._element_duration - self._fadeout_time, self._element_duration)]
            self._alpha_list = [(0.3, 1), (1, 1), (1, 0.3)] if not alpha_list else alpha_list
            self._action_num = 3

    def init_outputDesc(self):
        outputLocation = "*"
        outputAlphaLocation = "*"
        fps = 25.0
        duration = self._element_duration
        bgColor = "RGBA(0,0,0,255)"
        self._outputDesc = outputDesc.create(self._width, self._height, outputLocation, outputAlphaLocation, fps,
                                             duration, bgColor)

    def init_level(self):
        configDict = dict()
        configDict['id'] = 0
        configDict['name'] = "alpha"
        configDict['actionNumber'] = self._action_num
        configDict['elementNames'] = [self._elementNameFormat.format(configDict['name'], i) for i in
                                      range(configDict['actionNumber'])]
        configDict['newlevel_func'] = self.newLevel_Func
        configDict['newelement_func'] = self.newelement_Func
        configDict['baseTime'] = 0
        self._levelConfigs.append(configDict)

    def newLevel_Func(self, configDict):
        levelName = configDict['name']
        times = self._times
        baseActionDict = {
            "name": levelName,
            "element": configDict['elementNames'],
            "startTime": times[0][0],
            "endTime": times[0][1],
            "projectionType": "normal",
            "startPos": "0,0,1,1",
            "endPos": "0,0,1,1",
        }
        if self._action_configDict:
            baseActionDict.update(self._action_configDict)
        kwargs = {
            'element': configDict['elementNames'],
            'startAlpha_endAlpha': self._alpha_list
        }

        level = self.create_level_from_action(baseActionDict, configDict, times, **kwargs)
        return level

    def newelement_Func(self, configDict):
        names = configDict['elementNames']
        for i, name in enumerate(names):
            element = {
                'name': name,
                'source': 'designer',
                'type': self._element_type,
                'value': self._user_element
            }
            if self._element_configDict:
                element.update(self._element_configDict)
            if self._element_type == "video":
                video_prop = {
                    'videoProp': {
                        'startTime': self._times[i][0],
                        'endTime': self._times[i][1]}
                }
                element.update(video_prop)
            self._elements.append(element)


def test_effect():
    userVideo = "https://videofactory.oss-cn-shanghai.aliyuncs.com/ios/video/mv_7.mp4"
    videoDuration = 12000
    rotateVideo = make_Video(BPFade, userVideo, element_duration=videoDuration, fadeinTime=2000, fade='out')
    print(rotateVideo)


if __name__ == "__main__":
    test_effect()