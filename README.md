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

- **Interactive Features**: The Get Involved page is a hub for community action, featuring an interactive map that allows supporters to add a pin marking their location, visually showcasing the breadth and reach of the movement's support.

## Movement Map
### Movement Map Key Features
- **Interactive Map:** The movement map is an interactive feature powered by Leaflet.js. This map displays the locations of Little Falls supporters, events, and points of interest related to the movement.
- **Marker Placement:** Users can click on the map to add their own markers, thereby indicating their location or the location of a point of interest.
- **Marker Message: Users are given the ability to attach a custom message to the marker they place on the map.
- **Mobile-friendly:** The map is designed to be responsive, which means it scales and adjusts to provide a suitable user experience across a range of devices, including desktop computers, laptops, tablets, and smartphones.
### Movement Map Technical Details
- **Leaflet.js:** The map uses Leaflet.js, a popular open-source JavaScript library for interactive maps. Leaflet is lightweight, flexible, and efficient, making it ideal for this type of interactive web map.
- **Map Tiles:** OpenStreetMap tiles are used for the map. OpenStreetMap is a free and open-source collaborative mapping project.
- **Markers from DynamoDB: The markers are loaded from a DynamoDB database. This is accomplished by making a fetch request to an API, which returns the marker data. This data includes latitude and longitude coordinates, which are used to place the markers on the map.
- **Map Interaction:** When a user clicks on the map, the Leaflet.js library provides the latitude and longitude of the clicked point. The user can input a message, which can be associated with the marker.
Responsive Design:** CSS is used to ensure the map is responsive and works well on a range of device sizes. The map container is designed to scale based on the width of the viewport, while maintaining a fixed height.

### Movement Map Lambda Function
This section details the AWS Lambda function responsible for managing markers on the movement map.

#### Key Components
- `AWS` and `DynamoDB.DocumentClient`: These are part of the AWS SDK for JavaScript, used for interacting with AWS DynamoDB.
- `uuidv4`: Generates a unique identifier (UUID) for each new marker.
- `headers`: Contains headers for the HTTP response to allow cross-origin resource sharing (CORS).
- `addMarker`, `getMarkers`, `deleteMarker`: These async functions add a marker, retrieve all markers, and delete a marker from the DynamoDB table respectively.

#### Environment Variables
- `MARKER_TABLE`: The name of the DynamoDB table where markers are stored.

#### Execution
The execution of this script depends on an incoming event from AWS API Gateway. The event will contain the HTTP method (like `GET`, `POST`, `DELETE`, etc.) which will determine which function (`addMarker`, `getMarkers`, `deleteMarker`) will be executed. 

#### Dependencies
- `aws-sdk`: The official AWS SDK for JavaScript, available on NPM, used to interact with AWS services like DynamoDB.
- `uuid`: This library is used to generate unique IDs for each marker. The particular import `v4` generates a random UUID. 

#### Deployment
This script is deployed as an AWS Lambda function and is triggered by events from AWS API Gateway. Ensure the environment variable `MARKER_TABLE` is set with the name of your DynamoDB table and that your Lambda function has the necessary IAM permissions to interact with DynamoDB.

## Meta Tags Management
### Meta Tags Management Key Features
- **Automated Meta Information:** The site leverages Hugo's capabilities to dynamically generate meta information for each page. This is accomplished using Hugo variables to extract necessary data directly from markdown files, providing a highly efficient, automated process.
- **Unified Meta Tags Partial:** All meta tags are consolidated within a single partial, simplifying management and ensuring consistent implementation across all pages. 
- **SEO Optimization:** Proper usage of meta tags contributes to search engine optimization, enhancing the site's visibility on search engines.
- **Enhanced Social Media Sharing:** Open Graph and Twitter card tags are employed to optimize the appearance of shared links on social media platforms, generating engaging, detailed link previews.

### Meta Tags Management Technical Details
- **Hugo Variables:** Hugo's template variables are utilized to dynamically pull data from each markdown file when the site is generated. For instance, `{{ .Title }}` fetches the title of the current page.
- **Meta Tags Partial:** A dedicated partial file houses all the meta tags, included in the header of each page. This approach guarantees that every page carries the necessary meta tags, and maintains consistency throughout the site.
- **Open Graph and Twitter Cards:** These meta tags are used to generate rich previews of the site's content when shared on social media platforms, including elements such as title, description, and a relevant image.
- **Canonical URLs:** Canonical URLs are employed to specify the primary version of a page for search engines, crucial when multiple versions of a page exist, particularly in multilingual sites.
- **Fallbacks:** Fallback values are set for descriptions and other fields that may not always be provided in the page's front matter. This practice ensures a suitable value is always present for each meta tag.

In summary, this approach to managing meta tags not only bolsters SEO but also streamlines the process of maintaining consistency across all pages.

## Scrollytelling Experiences

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