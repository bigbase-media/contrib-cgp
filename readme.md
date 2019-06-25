#### BPFade 
    
    user_element:       The user material
    width:              Width of the video, default value is 720 
    height:             Height of the video, default value is 1280
    element_duration:   Duration of video 
    action_configDict:  Provide users with the ability to modify 
                        the configuration of internal actions with caution
    element_configDict: Provide users with the ability to modify 
                        the configuration of internal element with caution
    fadeinTime:         Duration of fading in.
    fadeoutTime:        Duration of fading out. 
    fade: 
                        None: Add fade-in and fade-out elements
                        in: Add fade-in elements
                        out: Add fade-out elements 
    alpha_list:         Transparency control list
    
    
###### Examples of video:
 <video>
    <source id="map41" src="http://test-v.oss-cn-shanghai.aliyuncs.com/hypnos-blueprint/output-11104-484360.mp4" type="video/mp4>
 </video>