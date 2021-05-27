# HowBusyIsToon: Getting started

## What is howbusyistoon (HBIT)?

The original HBIT was developed in spring 2020 to help support a safe return to the city centre after the first C19 lockdown. We knew that some people felt nervous about returning to crowded areas and we wanted to use the urban open data available in the city (on footfall and parking levels) to help give people confidence about how busy the city centre was. The prototype was a big success with positive user feedback and interest from other cities and stakeholders. We were successful in receiving MHCLG C19 digital funding and undertook more user research to inform a new version with more features which launched in November 2021 to support the busy Christmas shopping period.

## What are the benefits of HBIT? What problem is HBIT trying to solve?

HBIT allows you to present back data and information about your high street, town, or city to potential visitors which empowers them to make their own decisions. In Newcastle we wanted to support more people to make the decision to come into the city centre and feel reassured by the safety measures in place. This is vital in the economic recovery of our city post Covid. However, we also know of other user groups who are less concerned about the virus and more interested in quieter times to visit for other reasons, for example carers supporting vulnerable people. We also have user feedback that people find it interesting just to see the regular images of our city centre. 

Before we developed HBIT we had been collecting information on footfall and parking levels for many years but hadn’t been proactively sharing these with the general public. Since going live with HBIT we’ve had over 70,000 visits to the site, with lots of positive feedback.        

## How do I know that HBIT was informed by user needs?

The user research undertaken by Hedgehog Lab reached far and wide – you can see some of the findings in our research report here and our show and tell videos and presentations here. We continue to listen to user feedback through our onsite feedback form. The most frequent request is for additional camera views. We also know that there is continued demand for the site, with usage increasing 2,800% at the opening of non-essential retail on April 12th 2021.
How can I use HBIT in my town/city?  

## HBIT has a number of different features as shown in the table below. 

| Feature |	Summary	| Technical requirements |
| ------- | ------- | -----------------------|
| User research on how people feel about returning to crowded areas post lockdown. | Findings in relation to needs and wants from a cross section of respondents about returning to the city centre. | None. |
| Webpage showing how busy an area is | Code available on GitHub for webpage layout and structure. | • You will need a server or hosting for the website.<br>You will need access to a CCTV feed and a PC on the same network as the CCTV camera to push images out to the website.<br> • You will need access to a powerful computer for machine learning (or a purpose-built device) if you want to show busyness as a traffic light status or number. |
| Webpage showing safety measures in place |	Code available on GitHub for webpage layout and structure. | • You will need a server or hosting for the webpage and to provide content relevant for your area. |
| Webpage showing information on shops and restaurants |	Code available on GitHub for webpage layout and structure. | • You will need a server or hosting for the webpage and to provide content relevant for your area.<br> • You will need a Google Maps API key, obtainable by following these instructions. |
| Webpage showing how busy and area is and information on public transport and parking | Code available on GitHub for webpage layout and structure.	| • You will need a server or hosting for the webpage and to provide content relevant for your area.<br> • You may need access to real time information from sensors (for example on parking availability) if you want to share this. |

## How does HBIT meet privacy requirements?

Operating a camera in a public space that views pedestrians and their activity involves processing personal data and needs to comply with the Data Protection Act 2018.

The cameras we use in Newcastle provide the website with a regular still image, but are also used by a system that undertakes pedestrian counting using computer vision and machine learning. This allows us to generate a traffic light status which we share on the site. On our website, the information is transmitted back to the Urban Observatory and the website is automatically updated using the data collected. The footage is not routinely monitored. More information is available for Newcastle’s setup in the Urban Observatory's privacy statement. Your own implementation may vary however, depending on the setup of your network.
In your city, town, or location you can use HBIT with or without the pedestrian counting technology. Any camera deployment monitoring a public space is likely to require you to complete a Data Protection Impact Assessment (DPIA). (Luke - Can we give example?)

The Information Commissioner’s Office offers further guidance on the steps you need to take to comply with the legislation and prepare a DPIA. Your organisation’s data protection officer will likely need to review and approve this before you can proceed.

## I already have existing CCTV cameras – how do I get started? 

Many high streets already have CCTV cameras and the necessary power and data infrastructure. These might be operated by shopping centres, local authorities or the police for public safety and crime prevention. Most modern cameras produce a constant video stream and transmit it to a control room, where an operator can direct the camera, or to a recording device if it’s not continuously monitored. Most of these systems are digital, making it easy to stream the images into other software if the system supports standards like RTSP and ONVIF. If your camera supports either of these standards, then it should be possible to make it work.
We’re going to publish some example scripts in the coming weeks.

## I also want to start using my camera feed for pedestrian counting – what do I need to do? 

You should first consider if it’s feasible to count pedestrians using other technologies: an area of low footfall might be suitable for radar-based counting, or mobile operator data might be a suitable proxy for an estimate of people in an entire region. Our experience is that camera-based counting is most suitable only for busy streets, wide open spaces such as squares, and where there’s a high vantage point.

Next you need to consider if your CCTV cameras are suitable – for example fixed cameras pointed in a specific direction are preferable to pan-tilt-zoom cameras controlled by an operator which would provide different values depending on its position.

When it comes to processing the images into meaningful statistics such as pedestrians-per-minute there are further technical requirements. A sophisticated open-source model such as Microsoft Research’s FairMOT can do this processing in real time by offloading some of the processing from your PC’s main processor (your CPU) to graphics hardware (a GPU using CUDA) while simpler models can even run on a mobile phone. 

If you want to count pedestrians across a large number of cameras, you will need a significant number of high-specification gaming PCs, a datacentre setup, or a comparatively expensive cloud arrangement. If this applies to you we suggest looking at commercial options tailored specifically to pedestrian counting from CCTV instead. Commercial providers exist for specialised hardware that perform the counting within the camera unit or nearby (a form of edge processing) which can be more cost effective.

_We’re going to publish a detailed example of how to install and configure an open-source counting system in the coming weeks._

## I don’t have any CCTV cameras – what are my options?
The HBIT product still delivers value to users beyond busyness and you should consider how you can still give confidence by sharing information about safety advice and shops and restaurants using the research and code available. If you want to include busyness then other ways of collecting this type of information are set out above and range from clipboard surveys to using mobile phone data.

## What sort of hosting do I need for the site?
The main part of the website uses a static site generator tool called Hugo, which produces output files that contain everything the browser needs, and almost any web server setup should be able to host these files (e.g. Microsoft IIS, nginx, Apache). However, if you’re feeding in data from CCTV or car parking then an extra service is required to run alongside the website to handle this data; you’ll need to install a Python distribution (e.g. Anaconda) on your server for this part. It should be possible to use either Windows or Linux servers for the website.

If you or your IT department are comfortable using Linux servers (we run our servers on Ubuntu LTS but you don’t have to) then the easiest way to get the site up and running is using Docker. The GitHub repository contains scripts for the whole deployment process when using Docker, so you only need to type one command. We recommend this option.

## How do I change the content of the site?

Each page of the website has a file in the content directory. The page titles and style are described at the top of the file and then the content follows; menus are built automatically using the content of these files. The content of the pages can be written in HTML or Markdown, which is the format used by sites like Wikipedia. If you change these files you’ll need to run the site generator again (or restart the stack if using Docker) before the pages update.
How do I change the look and feel of the site?

Details like the menus can be changed in the same way as the content of the pages but it’s a little harder to change details like the fonts and text sizes. These are described in a series of SASS files in the assets directory. Most web developers will be familiar with this format.
How do I make sure the CCTV network remains secure?

We suggest you have a PC on the CCTV network that takes snapshots from the cameras and coordinates the counting, behind your firewall and segregated from your other network traffic. The snapshots and count results can then be pushed out through your firewall onto the web server, meaning traffic only ever travels in one direction and the web server has no way into your CCTV network. You’ll probably want to liaise with your network security and CCTV teams to set this up properly, with restrictions on which addresses can be contacted. There are many other ways to make it work securely though.
What should be my next steps? 

You need to consider:
1.	What are the user needs for your locality? Do you need to share images and/or pedestrian count information or just information about safety measures? 
2.	Do you have access to a CCTV network? If not, is this something you need to resolve?
3.	Do you want automated counting from the CCTV cameras or to publish images every few minutes? If you’re doing either of these then prepare a DPIA and work with your security and IT teams to make sure it can be done safely.
4.	What access to skills and resources do you have? We would recommend that you have access to the following core team
    *	political/executive sponsorship 
    *	web content/communications 
    *	web developer (with knowledge of HTML and Markdown to change the content, and CSS to change the overall look and feel)
    *	CCTV network manager (whoever has detailed knowledge of camera models, protocols, IP addresses etc.)
    *	If you want implement pedestrian counting from your CCTV you will also need a powerful PC (with an NVIDIA graphics card that supports CUDA) and someone with experience using the Linux operating system, or a commercial system for CCTV counting with an API.

## What is the roadmap for HBIT?  

_TBC_


