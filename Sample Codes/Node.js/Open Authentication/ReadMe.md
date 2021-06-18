# Node.JS Sample Code SSG-WSG
## Introduction
This Sample Code serves as a guide on calling a subscribed API through Open Authentication
### The design of the Sample Code
The Sample Code uses a two step process in order to successfully call a subscribed API
1. Retrieve a token based on the User's Client Id and Secret
2. Call a subscribed API based on the token retrieved
## Prerequisites
The following three prerequisites are required to run the sample code successfully
1. [A SSG-WSG Developer Account](https://developer.ssg-wsg.sg/webapp/guides/13EgI9eYfms1W7Ls4X1hdI)
2. [Ensure the Account is subscribed to an API with Open Authentication](https://developer.ssg-wsg.sg/webapp/guides/6gvz7gEnwU2dSIKPrTcXnq)
3. [NodeJS installer](https://nodejs.org/en/download/)
## How to use
1. Download the sample code
2. Open CMD and run the following commands
```
//To install necessary library
npm install prompt
npm install xmlhttprequest

//To run the program
node SampleCode.js
```
3. Enter the Client Id follow by Secret*

**The Client ID and Secret values can be obtained from the Developer Portal*


