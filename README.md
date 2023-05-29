<h1 align=center>Little Falls, VA Website</h1> 
<p align=center>The Little Falls, VA website advocates for the renaming of Falls Church, Virginia to Little Falls. It's built on Hugo framework using the Vex Hugo theme.</p>
<h2 align="center"> <a target="_blank" href="https://littlefallsva.com" rel="nofollow">Website</a></h2>

<p align=center>
  <a href="https://github.com/ryanmio/Little-Falls-VA">
    <img src="https://img.shields.io/github/license/ryanmio/Little-Falls-VA" alt="license"></a>

  <img src="https://img.shields.io/github/languages/code-size/ryanmio/Little-Falls-VA" alt="code size">

  <a href="https://github.com/ryanmio/Little-Falls-VA/graphs/contributors">
    <img src="https://img.shields.io/github/contributors/ryanmio/Little-Falls-VA" alt="contributors"></a>

</p>

---

<p align="center">
  <img src="https://littlefallsva.com/images/screenshot.png" alt="website screenshot" width="100%">
</p>

---

## Website Key Features

- **Multi-Lingual Support**: The site supports both English and Spanish

- **Press and Media Kit**: The press section is equipped with press releases and media kit

- **Inclusive History**: The site features an engaging scrollytelling experience about the history of Falls Church, covering everything from pre-colonial roots and indigenous presence to the civil rights era. 

- **E-commerce Store**: The site includes a store for supporters to purchase print-on-demand merchandise. 

- **Google Sheets Integration**: The petition features an embedded Google Script form that synchronizes with Google Sheets, allowing for real-time data collection from supporters in Google's free and familiar UI.

- **CRM Integration**: The site features a newsletter signup for updates on the renaming movement, upcoming events, and ways to contribute. Signups and petition signatures are processed through Netlify to a custom-built CRM.

- **Get Involved Page**: The Get Involved page is a hub for community action, featuring an interactive map that allows supporters to add a pin marking their location, visually showcasing the breadth and reach of the movement's support.

## History of Falls Church Scrollytelling Page

### Scrollytelling Key Features
- **Section-Based Progression:** As users scroll down, they move through distinct sections of the story. Each section represents a different chapter in Falls Church's history, and contains a mix of text, images, and interactive elements to convey that part of the story.

- **Synchronized Visual Elements:** Our scrollytelling approach includes synchronization between the user's scroll position and the visual elements displayed on the screen. This could be graphical elements (like maps or graphs changing over time), CSS animations (like an image fading in or out), or text (like a new piece of narration appearing).

- **Interactive Visualizations:** In certain sections, users can interact with the visualizations to explore more about the topic at hand. This enhances user engagement and allows for a deeper understanding of the content.

### History Scrollytelling Techincal Details
- **Scrolling Logic:**
The scrolling interaction is powered by the IntersectionObserver API in JavaScript, which provides a way to asynchronously observe changes in the intersection of a target element with an ancestor element or with a top-level document's viewport.

This API is used to detect when the user has scrolled to a new section of the history. Each "waypoint" section element has an IntersectionObserver attached to it, which triggers the progression of the story when the section comes into view.

When a new waypoint comes into view, the associated content is made visible using CSS classes, and the inView data attribute of the waypoint is updated to control the flow of the story.

- **Animation:**
The animations are achieved using the Web Animations API. This is a modern, promise-based API that provides a way to create animations directly in JavaScript, without needing to use CSS animations or the requestAnimationFrame method.

Different animations are created for each section of the story. These animations are stored in a JavaScript object and are triggered when their associated section becomes the active section (i.e., when it comes into view).

- **Images and Media:**
Images and media are lazy-loaded using the IntersectionObserver API. This means they are only loaded when they come into view, which improves the performance of the site.

Each image has an IntersectionObserver attached to it. When the image comes into view, the data-src attribute of the image is set to the actual URL of the image, triggering the browser to load the image.

- **Responsive Design:**
The site is designed to be responsive, meaning it works well on both desktop and mobile devices. This is achieved by using CSS media queries to change the layout of the site based on the viewport size. The site also utilizes the ResizeObserver API to adjust the scroll interactions based on the size of the viewport.


### Nelly's Journey Scrollytelling Technical Details
- **Scrolling Logic:**
The scrolling interaction is powered by the IntersectionObserver API in JavaScript, which provides a way to asynchronously observe changes in the intersection of a target element with an ancestor element or with a top-level document's viewport.

This API is used to detect when the user has scrolled to a new section of the history. Each "waypoint" section element has an IntersectionObserver attached to it, which triggers the progression of the story when the section comes into view.

When a new waypoint comes into view, the associated content is made visible using CSS classes, and the inView data attribute of the waypoint is updated to control the flow of the story.

- **Animation:**
The animations are achieved using the Web Animations API. This is a modern, promise-based API that provides a way to create animations directly in JavaScript, without needing to use CSS animations or the requestAnimationFrame method.

Different animations are created for each section of the story. These animations are stored in a JavaScript object and are triggered when their associated section becomes the active section (i.e., when it comes into view).

- **Images and Media:**
Images and media are lazy-loaded using the IntersectionObserver API. This means they are only loaded when they come into view, which improves the performance of the site.

Each image has an IntersectionObserver attached to it. When the image comes into view, the data-src attribute of the image is set to the actual URL of the image, triggering the browser to load the image.

- **Responsive Design:**
The site is designed to be responsive, meaning it works well on both desktop and mobile devices. This is achieved by using CSS media queries to change the layout of the site based on the viewport size. The site also utilizes the ResizeObserver API to adjust the scroll interactions based on the size of the viewport.

## Repository Structure
<pre>
.
├── archetypes # Templates for generating new content
├── assets # Resources like SCSS or JavaScript files
├── exampleSite # Example or demo website content
├── images # Image files used on the website
├── layouts # HTML templates for rendering views of the content
├── netlify/functions/subscription-form-function # Netlify serverless function code
├── static # Static files to be copied directly to the root of the public directory
├── .gitignore # Specifies untracked files to be ignored by Git
├── LICENSE # License for the project
├── README.md # Information about the project
├── netlify.toml # Netlify configuration for the site
├── package.json # Lists the JavaScript dependencies of the project
└── theme.toml # Configuration for the Hugo theme
</pre>

<!-- licence -->
## License

Copyright &copy; 2023 Committee for Little Falls

**Code License:** Released under the [MIT](https://github.com/ryanmio/Little-Falls-VA/blob/master/LICENSE) license.

<!-- resources -->
## Special Thanks

- [Hugo](https://gohugo.io/)
- [Vex Hugo Theme](https://github.com/themefisher/vex-hugo)