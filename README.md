<h1 align="center">
  <a href="https://devpost.com/software/eyesafe"><img src="extension/assets/eyeSafe.jpeg" alt="eyeSafe - Keep you and eye Safe." width="400"></a>
  <br>
  eyeSafe - Keep you and eye Safe.
  <br>
  <br>
</h1>

<p align="center">
  <a href="https://github.com/QasimWani/LeetHub/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="license"/></a>
  <a href="https://github.com/alexquach/eyeSafe"><img src="https://travis-ci.org/dwyl/esta.svg?branch=master" alt="build"/></a>
  <a href="https://twitter.com/intent/tweet?text=eyeSafe%20-%20Keep%20you%20and%20eye%20safe!&url=https://github.com/alexquach/eyeSafe/&hashtags=eye-strain,health,devpost,coding,python,javascript,chrome"> <img src="https://img.shields.io/twitter/url/http/shields.io.svg?style=social"> </a>
</p>


### Check it out!

<table style="border-collapse: separate;"><tr>
  <td style="border-spacing:2em 0"> 
      <a href="https://www.youtube.com/watch?v=fJ4aXA5IY6Q">
        <img src="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2F1000logos.net%2Fwp-content%2Fuploads%2F2017%2F05%2FNew-YouTube-logo.jpg&f=1&nofb=1" alt="YouTube video" height=100 width=150/>
      </a>  
  </td>
  <td style="border-spacing:2em 0"> 
      <a href="https://devpost.com/software/eyesafe" target="_blank"><img src="https://devpost-challengepost.netdna-ssl.com/assets/reimagine2/devpost-logo-646bdf6ac6663230947a952f8d354cad.svg" alt="LeetHub - Automatically sync your code b/w Leetcode & GitHub. | Product Hunt" style="width: 150px; height: 100px;" width="250" height="54" /></a>

  </td>
</tr></table>

## To run locally:
- Clone this Repo
- `cd eyeSafe/flask`
- Start flask server
`$flask run`
- Upload extension/ folder to Chrome extension
- Go to 127.0.0.1:5000
- Browse!

## HealthTrack
## Inspiration
As many of us have been lucky enough to quarantine indoors for school and work, the amount of time spent on screens have skyrocketed. Doctors estimate that healthy blinking rates are 15-20 times per minute; however while using a computer, our blinking rates are about 1/3 of the healthy rate. This leads to eye strain, dryness, and unhealthy eye habits. We take on this challenge to influence human behavior with computer vision technology.

## What it does
eyeSafe uses your computer webcam to detect how often you blink. As you work at your computer, if the program detects that you have been underperforming in your blink rate it deploys changes to your browser. 
- performs active content enhancement to promote healthier blinking behavior
- encourages the doctors' recommended 20/20/20 rule by a fun challenge
- produces analytics over the timespan that you use the application. 

## How we built it
We used the following technologies:
- openCV (python) to continually detect and count the blinks from the video stream. We used the eye-aspect ratio (EAR) metric to detect blinks [cited here (2016)](https://vision.fe.uni-lj.si/cvww2016/proceedings/papers/05.pdf)
- flask to serve the extension
- chrome extension to interface with the user to start the service

## Challenges we ran into
Streaming video data from a web browser to a flask server was a challenging aspect of the project. 

## Accomplishments that we're proud of
We've reduced our eye strain by over 30%!

## What we learned
literally anything is possible.

## What's next for eyeSafe
Expand our analytics to also correlate blink behavior with certain activities/websites, and of course
Get acquired by Google!
