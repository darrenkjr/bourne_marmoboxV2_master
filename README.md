# bourne_marmoboxV2_master
MarmoboxV2 - Executive Code - To be Run on Main Server 

# Introduction
Project Marmobox is an automated, modular system for in cage operant conditioning of marmosets. It is a hardware + service that automates the training of marmosets in simple behavioural tasks, and allows for seamless interrogation of behavioural tasks and rudimentary data analysis and visualisation. 

Its purpose is to allow researchers or users to interrogate behaviour related questions whilst achieving: 

- Higher throughput
- More naturalistic behaviour in model animals
- Less human error
- More reproducible protocols
- More ethical treatment of animals (equating to lower stress levels, and quality of life for animals)

#Design Principles

To frame design work going forward, and to focus discussion so as to prioritise features, here are a few suggested principles to adhere to: 

- Design should be as modular as possible, for easy maintenance and debugging.
- Design should leave room for further expansion
- User intervention should be minimised as much as possible.
- Where possible, data cleaning, handling and presentation should be as standardised as possible. Where possible, rudimentary post hoc data analysis and visualisation should be automated.
- Code and user experience should be frictionless post set up.
- Design should be as ethically permissible as possible - Feature consideration should not compromise on animal stress levels where possible.
- Design should allow as much customisability from the operator as possible.
- Reproducibility and reliability of collected data is paramount.

This repository contains the code for the server (master) version of Marmobox version 2.

# Requirements
You must have python 3 or greater. 

#General architecture 

There are 2 repos associated dwith Project Marmobox. A central server that contains internal protocol logic, and child pcs that controls the stimuli and rewards for our animals. 

The central server, handles communication with a  SQL database, (To be run separately), and communicates with the child pc via json. The child pc consists of touchscreens, a 3D printed enclosure, and an arduino based system. 

#Difference with Marmobox V1

We've set up version 2 to tackle the folllwing shortomcings: 


- In essence, the processing power of Marmobox V1 is not sufficient for more graphically intensive tasks. CPU Processing bottlenecks result in unreliable data, especially during progression to non-static tests, such as motion coherence tasks, with more reliance on temporal data.
- Latency issues and jitters are hard to separate within the firmware, and there is no clear separation between:
    - the firmware required to run the Marmobox system alone - and progress through presentation of behaviour tasks
    - the Software and user experience when conducting post-hoc analysis and data visualisation
- As a result the intertwining of the code base results in hard to debug code, and makes it hard to quantify and detect bottlenecks, sources of jitter and lag, and address concerns with temporally precise measurement and analysis of data.
    - For example, metrics to do with temporal data, latency and reaction are unreliable without quantifying the extent of error, jitter and processing time within the system.
- There are non-essential portions that are executing on the microcomputer of Marmobox V1. This being elements such as the Pi Camera, the streaming of video, generation of reports, data visualisation etc. - A separation of these non-essential elements is important in order to reduce load on the computer to achieve the required precision.
- Current user experience is limited. Customisability by operator has not been a guiding design principle, as such thinking behind allowing variation in reward dispensing or modification of reward tones has been limited. This reflects in the **concrete limitations of the system and how these limitations came to be.**
- Furthermore, Marmobox V1 was built with no guiding design principles. Thus, current design rationale does not take into account what Marmobox should be able to achieve, focus on, and do well in. What should sit in the realm of the operator, and should be done by Marmobox?
    - A discussion between engineers + designers, along with potential users should be had to discuss the philosophy behind Marmobox as a project.

