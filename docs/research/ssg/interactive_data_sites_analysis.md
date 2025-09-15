# **A Technical Analysis of Static Site Generators for Client-Side Data Applications on GitHub Pages with Local CI/CD**

## **Executive Summary**

This report provides a comprehensive analysis of static site generator (SSG) architectures capable of supporting advanced client-side interactivity and a cost-effective, self-hosted CI/CD pipeline. The analysis identifies **Astro** and **Next.js (in Static Export mode)** as the leading candidates that align with all user requirements, with **Astro** emerging as the superior architectural choice due to its "islands" model and minimal JavaScript delivery. The report details the technical blueprint for each solution, including the integration of DuckDB-Wasm for in-browser data processing, D3.js for interactive visualizations, and the critical steps for deploying to GitHub Pages using a self-hosted GitHub Actions runner. The final recommendation is the **Astro-Centric Solution Architecture**, as it provides the optimal balance of performance, flexibility, and architectural elegance for this specific use case.

## **Section 1: Foundational Principles of the Modern Web Stack**

### **1.1 The Evolution of Static Sites: From Simple Files to Dynamic Frontends**

A static site generator (SSG) is a sophisticated software application that automates the creation of a complete website composed of static HTML, CSS, and JavaScript files from a set of raw data and templates.1 This process, which occurs at build time, fundamentally contrasts with the traditional content management system (CMS) approach.1 A CMS, such as WordPress, generates pages dynamically on the server in response to each user request by querying a database, applying templates, and then serving the finished page.1 Conversely, an SSG pre-builds every page, rendering them ready for instant delivery to the end user.1

This pre-rendering has a number of significant advantages. Firstly, because the pages are already built, they load exceptionally quickly, which provides a superior user experience and can contribute to better search engine optimization (SEO).2 Secondly, static sites are inherently more secure as they have no server-side processing or database to serve as a vulnerable attack surface.4 Finally, they are lightweight and require far fewer server resources, making them highly performant under scale.4

The modern architecture that leverages SSGs is known as the JAMstack, a methodology built on JavaScript, APIs, and Markup.1 In this model, the SSG handles the "Markup" by pre-building the HTML. Any dynamic functionality is offloaded to the "JavaScript" layer, which runs in the user's browser, and "APIs" are used for any required backend services.1

This report addresses a central paradox in modern web development. The query is for a "static site" that paradoxically supports highly dynamic, client-side functionality, specifically "in-browser data processing" and "animated graphs/charts".2 The traditional definition of a static site is one that "remains the same for every user and is not as interactive".2 The resolution of this apparent contradiction lies in the architectural maturity of the JAMstack. The "J" (JavaScript) component has evolved from a simple tool for basic interactivity to a powerful execution environment capable of running sophisticated applications, such as an in-browser database (DuckDB-Wasm) or a data visualization engine (D3.js). This capability allows a website to be delivered as a static artifact, yet provide a dynamic and personalized user experience without requiring a backend server. This progression shifts the primary point of differentiation between SSGs from their templating capabilities to their efficiency and flexibility in handling and delivering client-side JavaScript.

### **1.2 Comparative Analysis of Leading Static Site Generators**

The landscape of modern SSGs is characterized by a fundamental architectural divide. On one side are dedicated SSGs, which are optimized for generating static content and little else. On the other side are multi-rendering frameworks that support static site generation as one of many deployment options, alongside Server-Side Rendering (SSR) and Client-Side Rendering (CSR).2 The user’s requirements for advanced client-side interactivity necessitates a multi-rendering framework, as these tools are designed to manage and optimize complex JavaScript applications.

The leading candidates for this project are:

* **Astro:** A relatively modern, framework-agnostic SSG that distinguishes itself with its "Islands Architecture".3 This philosophy dictates that Astro ships zero JavaScript to the client by default, delivering only static HTML and CSS.3 Interactivity is introduced by selectively "hydrating" specific components (or "islands") with the necessary JavaScript.5 This unique approach allows for significant performance gains, as the final bundle size is drastically reduced, and pages load much faster than with frameworks that hydrate the entire application.5 Astro also provides the flexibility to mix and match different frontend frameworks—such as React, Vue, and Svelte—within the same application, a feature that allows a development team to leverage different tools for specific tasks.5  
* **Next.js (Static Export):** An open-source, React-based framework backed by Vercel.2 Next.js can be configured to produce a static export, which generates a complete set of static HTML, CSS, and JavaScript files in an  
  out folder.6 This output can then be deployed to any static host, including GitHub Pages.6 Next.js supports client-side data fetching, a feature that allows a page to be pre-rendered as a static file and then populated with dynamic data via JavaScript after it has loaded in the browser.7 The Next.js ecosystem is vast and mature, with widespread enterprise and community adoption.8  
* **Gatsby:** A highly popular React-based framework that uses GraphQL as a central data layer.2 Gatsby is known for its extensive plugin ecosystem and its ability to pull data from a wide variety of sources, which it unifies via its GraphQL API.5 The framework compiles modern JavaScript and GraphQL into static HTML and CSS and then "re-hydrates" the application after it loads, providing the feel of a single-page application (SPA).8 A significant drawback of this approach, particularly when compared to Astro, is that Gatsby tends to ship a heavier JavaScript bundle, which can lead to longer build times and slower initial page loads.3 The GraphQL layer also presents a learning curve for developers unfamiliar with the technology.5  
* **Eleventy (11ty):** A dedicated SSG written in JavaScript.2 Eleventy is celebrated for its simplicity, flexibility, and independence from any specific frontend framework.8 It is a compelling choice for developers who prefer to work with vanilla JavaScript and Node.js.2 While this simplicity is a strength, it also means that the developer is entirely responsible for managing all aspects of client-side interactivity and the associated complexity, which may be a more manual process than with a purpose-built framework like Astro or Next.js.

The architectural philosophies of these frameworks represent a critical distinction. Next.js and Gatsby, by default, build and hydrate the full application on the client. In contrast, Astro's Islands Architecture is a direct counter-approach, targeting the problem of "heavy JavaScript" and slow build times that developers have faced with the full-hydration model.3 This fundamental difference in how client-side JavaScript is handled directly impacts performance and developer experience, making Astro's model uniquely suited to a project where interactivity is a key requirement but must not come at the cost of overall site speed. The following table provides a concise summary of the key SSG candidates.

**Table 1: Key SSG Comparison Matrix**

| SSG | Primary Language/Framework | Client-Side JS Model | Build Speed | DuckDB-Wasm Integration | D3.js Integration | GH Pages Compatibility |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| **Astro** | JS/Astro | Islands | Very Fast | Yes | Yes | Yes |
| **Next.js** | React | Full Hydration | Fast | Yes | Yes | Yes |
| **Gatsby** | React/GraphQL | Full Hydration | Moderate | Yes | Yes | Yes |
| **Eleventy** | JS | Manual | Fast | Yes | Yes | Yes |

## **Section 2: The Client-Side Data Ecosystem**

### **2.1 In-Browser Data Processing with DuckDB-Wasm**

DuckDB is a high-performance in-process SQL OLAP database management system that has been compiled to WebAssembly (Wasm).10 This compilation allows the database to run directly inside any modern web browser.11 The DuckDB-Wasm client provides a complete, embeddable SQL engine for performing complex analytical queries on data without a network round trip to a server.10

A successful DuckDB-Wasm deployment is not as simple as including a single JavaScript file. The system requires three primary components to be served correctly 13:

* **The main library component:** Distributed as a TypeScript or JavaScript package, this component needs to be bundled with the application and must know the locations of the other files it depends on.13  
* **The JavaScript Worker component:** This file is responsible for running the database in a separate browser thread to prevent blocking the main UI thread. It comes in different flavors (mvp, eh, threads) to support varying WebAssembly specifications and performance characteristics.13  
* **The WebAssembly module:** The core database engine itself, compiled as a .wasm file, must be served as-is from a reachable domain.13

The correct serving of these interconnected files is a non-trivial requirement that highlights a direct dependency on the chosen SSG's build system. A SSG that makes it difficult to manage and place these specific file types would be a poor choice. The existence of official examples with modern bundlers and frameworks like Vite and SvelteKit demonstrates that a framework-based SSG is the most natural and well-supported environment for integrating this sophisticated technology.14 A static site generator called "Evidence" even uses a client-side DuckDB-Wasm instance to run queries at runtime on pre-generated Parquet files, a concrete proof-of-concept for the exact use case described in the query.15

### **2.2 Creating Interactive and Animated Data Visualizations with D3.js**

D3.js is a premier JavaScript library for creating bespoke data visualizations. It is not a high-level charting library in the traditional sense; rather, it is a low-level "toolbox" of powerful primitives for binding arbitrary data to the Document Object Model (DOM) and applying data-driven transformations.16 This granular control offers unparalleled flexibility for creating custom, dynamic, and interactive visualizations.16

D3.js is explicitly designed for interactivity.16 Its core functionality includes

selections and transitions to create, update, and animate DOM elements based on data.16 It also provides features for

interactions such as panning, zooming, brushing, and dragging, which are essential for exploratory data analysis.16 This functionality allows a user to directly manipulate a chart and see the results in real time, making the data feel tangible and responsive.

The integration of D3.js with component-based frameworks like React (used by Next.js and Gatsby) and Svelte (supported by Astro) is a well-established pattern.19 A common approach involves using a

useRef hook to obtain a reference to the SVG container where the visualization will be drawn.19 The D3.js rendering logic is then placed within a

useEffect hook, ensuring that the visualization is created or updated after the component has mounted or its data dependencies have changed.19 This pattern elegantly delegates lifecycle management to the framework while allowing D3.js to perform its specialized low-level DOM manipulation, creating a seamless and powerful combination.

The two core interactivity requirements of the project—DuckDB-Wasm and D3.js—are deeply and synergistically linked. DuckDB-Wasm serves as the in-browser analytical engine, providing the means to perform complex SQL queries on a dataset.12 D3.js, in turn, is the visualization engine that can consume the results of those queries.15 This creates a complete, self-contained, client-side data pipeline: a user's action (e.g., clicking a button) can trigger a JavaScript function that executes a query on a local DuckDB-Wasm instance. The resulting data is then passed directly to a D3.js component, which efficiently renders or animates a new chart based on the query's output. This powerful, end-to-end loop is possible only with an SSG architecture that excels at managing and delivering sophisticated client-side JavaScript applications.

## **Section 3: Architecting the Deployment Pipeline**

### **3.1 Deploying Static Sites to GitHub Pages: Overcoming the SPA Challenge**

GitHub Pages is a free hosting service that allows for the deployment of static websites directly from a GitHub repository.21 The standard deployment process is straightforward: a developer pushes the static site files to a designated branch (

main or gh-pages) in the repository, and GitHub Pages automatically serves the content.21 The service is an excellent choice for a cost-free static site host.

However, a significant challenge arises when deploying a single-page application (SPA) to GitHub Pages. SPAs manage routing on the client side, meaning that all "pages" are dynamically loaded into a single index.html file without a full page refresh.23 This works perfectly for internal navigation (e.g., clicking a link from the home page to the

/about page) because the client-side router (such as React Router) intercepts the click and handles the transition.23 The problem occurs when a user attempts to navigate directly to a specific SPA route (e.g.,

user.github.io/repo/about) by typing it into the browser's address bar or refreshing the page.24 The GitHub Pages server, which is unaware of the SPA's internal routes, looks for a file named

about.html and, not finding it, returns a 404 error.24

To resolve this issue and enable full, direct URL support, a clever workaround must be implemented. The solution leverages the custom 404.html file feature of GitHub Pages.24 The process is as follows:

1. A request for a non-existent URL (like /about) is made to the server.  
2. The GitHub Pages server, upon returning the 404 error, is configured to serve the custom 404.html file instead of the standard error page.24  
3. The 404.html file contains a small JavaScript script that captures the original URL and then performs a client-side redirect back to the index.html page, passing the original path as a query parameter.24  
4. The index.html file, which must contain a second script loaded before the main SPA script, checks for this query parameter.  
5. If the original path is found, the script uses the window.history.replaceState() API to replace the current URL in the browser's address bar with the correct, original URL (user.github.io/repo/about) without triggering a new page load.24  
6. The SPA's router then loads the correct component for the now-valid URL.

This pragmatic fix is not an optional detail but a critical, non-obvious step that is essential for a professional and user-friendly web application. It transforms a static hosting limitation into a functional solution, demonstrating that even a "static" architecture requires careful consideration of the deployment environment.

### **3.2 The Self-Hosted Runner: A Cost-Effective CI/CD Solution**

The user's requirement for a cost-controlled CI/CD pipeline points directly to the use of self-hosted GitHub Actions runners.26 While GitHub provides free minutes for its hosted runners on public repositories, private repositories have a limited quota, after which charges are incurred.26 Self-hosted runners, on the other hand, are completely free to use, regardless of whether the repository is public or private, which directly eliminates the possibility of incurring any billing.26

A self-hosted runner is a system—which can be a physical machine, a virtual machine, or a container—that is set up and managed by the developer to execute GitHub Actions jobs.28 The setup process is a one-time effort that involves downloading the runner application and running a

config script to register it with the GitHub repository.29 The runner machine then polls GitHub for pending jobs and executes them when a workflow is triggered.30

The CI/CD pipeline for the static site is defined in a YAML file located in the .github/workflows/ directory of the repository.31 This file defines a job that uses the

runs-on: self-hosted directive to specify that the self-hosted runner should be used.32 The workflow typically triggers on a

push event and contains a sequence of steps:

1. **Checkout Code:** The actions/checkout action is used to clone the repository's code onto the runner machine.31  
2. **Install Dependencies:** Node.js dependencies are installed using a command like npm ci.22  
3. **Build Site:** The SSG's build command (npm run build) is executed to generate the static files.33  
4. **Deploy:** The generated static files are deployed to the appropriate location, such as a designated branch for GitHub Pages.22

This cost-effective solution is not without its trade-offs. The "free" aspect of self-hosted runners comes with the responsibility of managing the underlying hardware and software.28 This includes the initial provisioning and configuration of the machine and the ongoing maintenance of the operating system, security, and updates.28 This is a classic engineering decision: a developer can choose to pay for the convenience of GitHub's managed, hosted runners or invest time and effort to manage their own environment to avoid costs. The following table provides a clear breakdown of this trade-off.

**Table 2: CI/CD Cost and Management Comparison**

| Runner Type | Billing Model (Private Repo) | Management Overhead | Ideal Use Case |
| :---- | :---- | :---- | :---- |
| GitHub-hosted | Charged per minute after quota | Very low (GitHub manages infrastructure) | Projects with low build frequency or when cost is not a primary constraint. |
| Self-hosted | Free | High (user provisions and maintains hardware/software) | Projects with frequent builds where cost prevention is a key requirement. |

## **Section 4: Integrated Solutions and Recommendations**

Based on the detailed analysis, two primary SSG architectures stand out as the most suitable for this project: the Astro-Centric Solution and the Next.js Static Export Solution. Both can fully meet all of the user's requirements, but they approach the problem from different architectural philosophies.

### **4.1 The Astro-Centric Solution Architecture**

This solution leverages Astro's unique architectural model to deliver a highly performant static site. The core principle is to build the majority of the site as static HTML and only embed JavaScript for the specific, highly interactive components that require it.

**Implementation Roadmap:**

1. **SSG Setup:** Initialize a new Astro project, which comes with out-of-the-box support for popular frameworks.  
2. **Interactive Component:** Create a client-side component (e.g., DuckDBDashboard.astro) that encapsulates all the interactive logic. Within this component, import the DuckDB-Wasm and D3.js libraries. The component's JavaScript will handle the entire client-side data pipeline: fetching data files (e.g., Parquet or CSV), executing SQL queries with DuckDB-Wasm, and passing the results to a D3.js chart for rendering and interactivity. The Astro build process will correctly serve the necessary DuckDB-Wasm and D3.js files, ensuring they are available to the browser.  
3. **Deployment:** Configure the Astro project to output its static files to a designated directory, such as docs or dist. Implement the custom 404.html workaround to ensure that SPA routing functions correctly on GitHub Pages.  
4. **CI/CD Pipeline:** Set up and configure a self-hosted runner on a local machine by following the GitHub Actions documentation. Create a .github/workflows/main.yml file with a workflow that triggers on a push to the main branch. The job will use the runs-on: self-hosted directive to execute on the local runner. The workflow will contain steps to install dependencies, run the Astro build command, and then push the generated static files to the appropriate GitHub Pages branch (e.g., gh-pages).

### **4.2 The Next.js Static Export Solution Architecture**

This solution uses Next.js in its static export mode, providing a robust, React-based foundation for the project. Next.js's mature ecosystem and powerful features make it a strong contender, even when not leveraging its server-side capabilities.

**Implementation Roadmap:**

1. **SSG Setup:** Create a new Next.js project and modify the next.config.js file to enable the static export feature by setting output: 'export'.6 This configuration tells Next.js to produce a static site rather than a server-ready application.  
2. **Interactive Component:** Build a React component that contains the DuckDB-Wasm and D3.js logic.19 The component will use a  
   useRef hook to manage the SVG element and a useEffect hook to run the D3.js rendering logic after the component mounts.19 This component will be responsible for fetching data, running SQL queries with the DuckDB-Wasm instance, and updating the chart in response to user interactions.  
3. **Deployment:** Run the next build command, which will generate a static site in the out directory.6 As with the Astro solution, a custom  
   404.html must be created and configured to handle the SPA routing issues on GitHub Pages.  
4. **CI/CD Pipeline:** The CI/CD setup is identical to the Astro-centric solution. A self-hosted runner is configured, and a GitHub Actions workflow is created to trigger on a push, use the local runner, build the Next.js static export, and deploy the out folder's contents to the GitHub Pages branch.

### **4.3 Comprehensive Feature and Platform Comparison**

Both the Astro-centric and Next.js static export solutions are fully capable of meeting the project's requirements. They both seamlessly integrate client-side data processing and visualization, support deployment to GitHub Pages, and can be automated with a cost-free self-hosted CI/CD pipeline. However, a final comparison reveals a clear architectural advantage for Astro in this specific context.

Astro's Islands Architecture is a superior architectural fit for a static site that requires selective interactivity. While the Next.js static export will function correctly, it still carries the overhead of a larger JavaScript bundle due to its full-hydration model.3 For a data application where the majority of the content is static documentation or introductory material and only a few components are interactive data dashboards, Astro's approach of shipping minimal JavaScript by default offers a significant performance benefit.3

Furthermore, while both frameworks can be extended to support DuckDB-Wasm and D3.js, Astro's framework-agnostic nature provides an added layer of flexibility, allowing a developer to choose the best tool for each component.5 This flexibility can be a major advantage for future development and maintenance. The conclusion is that while Next.js is a very good choice, Astro is the optimal choice for this specific use case, directly addressing the performance drawbacks that have been identified in other full-hydration frameworks.3 The following table provides a final summary of the two leading solutions.

**Table 3: Solution Blueprint Matrix**

| Feature/Requirement | Astro-Centric Solution | Next.js Static Export Solution |
| :---- | :---- | :---- |
| **SSG** | Astro | Next.js (output: 'export') |
| **Client-Side Data Processing** | DuckDB-Wasm is integrated into interactive components. | DuckDB-Wasm is integrated into a React component. |
| **Animated Graphs/Charts** | D3.js is used within a client-side component. | D3.js is used within a React component via useEffect. |
| **Deployment to GitHub Pages** | Fully supported, requires 404.html workaround. | Fully supported, requires 404.html workaround. |
| **CI/CD** | Self-hosted runner with GitHub Actions workflow. | Self-hosted runner with GitHub Actions workflow. |
| **Architectural Strengths** | Minimal JavaScript bundles via Islands Architecture. | Mature ecosystem and widespread community support. |
| **Architectural Weaknesses** | Smaller community than Next.js. | Heavier JavaScript bundle compared to Astro. |

## **Conclusion**

The analysis demonstrates that building a highly interactive, data-driven static site on GitHub Pages with a cost-effective, self-hosted CI/CD pipeline is a viable and technically sound approach. The project requires a careful selection of tools and a precise architectural blueprint.

The primary recommendation is the **Astro-Centric Solution Architecture**. Astro's innovative Islands Architecture provides a definitive advantage by prioritizing performance through minimal JavaScript delivery, a crucial factor for a static site that must remain fast while supporting sophisticated, client-side functionality. This architectural elegance is a direct response to the performance challenges observed in other frameworks that hydrate the full application.

The integrated blueprint presented in this report provides a clear, step-by-step roadmap for a successful implementation. This includes:

* Astro as the foundational SSG for its performance and flexibility.  
* DuckDB-Wasm and D3.js as the core engines for in-browser analysis and bespoke visualization.  
* The 404.html workaround as the critical solution for GitHub Pages SPA routing.  
* A self-hosted GitHub Actions runner as the cost-free CI/CD engine.

By adhering to this architectural blueprint, a development team can create a robust, high-performance, and cost-effective data application that fully satisfies all the complex and interconnected requirements of the project.

#### **Works cited**

1. What is a static site generator? \- Cloudflare, accessed September 16, 2025, [https://www.cloudflare.com/learning/performance/static-site-generator/](https://www.cloudflare.com/learning/performance/static-site-generator/)  
2. Guide to Static Site Generators (SSGs) in 2024, Plus Top Options \- Prismic, accessed September 16, 2025, [https://prismic.io/blog/static-site-generators](https://prismic.io/blog/static-site-generators)  
3. Astro vs Gatsby: Is Astro becoming a replacement for Gatsby? \- DEV Community, accessed September 16, 2025, [https://dev.to/momciloo/astro-vs-gatsby-is-astro-becoming-a-replacement-for-gatsby-24d4](https://dev.to/momciloo/astro-vs-gatsby-is-astro-becoming-a-replacement-for-gatsby-24d4)  
4. What Is a Static Website? The Absolute Beginner's Guide \- Kinsta®, accessed September 16, 2025, [https://kinsta.com/knowledgebase/what-is-a-static-website/](https://kinsta.com/knowledgebase/what-is-a-static-website/)  
5. Astro vs Gatsby in 2025 for Developers \- Strapi, accessed September 16, 2025, [https://strapi.io/blog/astro-vs-gatsby-performance-comparison](https://strapi.io/blog/astro-vs-gatsby-performance-comparison)  
6. Guides: Static Exports \- Next.js, accessed September 16, 2025, [https://nextjs.org/docs/pages/guides/static-exports](https://nextjs.org/docs/pages/guides/static-exports)  
7. Rendering: Static Site Generation (SSG) \- Next.js, accessed September 16, 2025, [https://nextjs.org/docs/pages/building-your-application/rendering/static-site-generation](https://nextjs.org/docs/pages/building-your-application/rendering/static-site-generation)  
8. Our top 12 Static Site Generator (SSG) Picks for 2025 \- Hygraph, accessed September 16, 2025, [https://hygraph.com/blog/top-12-ssgs](https://hygraph.com/blog/top-12-ssgs)  
9. Eleventy \- YouTube, accessed September 16, 2025, [https://www.youtube.com/c/EleventyVideo](https://www.youtube.com/c/EleventyVideo)  
10. duckdb/duckdb-wasm: WebAssembly version of DuckDB \- GitHub, accessed September 16, 2025, [https://github.com/duckdb/duckdb-wasm](https://github.com/duckdb/duckdb-wasm)  
11. DuckDB Wasm, accessed September 16, 2025, [https://duckdb.org/docs/stable/clients/wasm/overview.html](https://duckdb.org/docs/stable/clients/wasm/overview.html)  
12. Guides \- DuckDB, accessed September 16, 2025, [https://duckdb.org/docs/stable/guides/overview.html](https://duckdb.org/docs/stable/guides/overview.html)  
13. Deploying DuckDB-Wasm – DuckDB, accessed September 16, 2025, [https://duckdb.org/docs/stable/clients/wasm/deploying\_duckdb\_wasm.html](https://duckdb.org/docs/stable/clients/wasm/deploying_duckdb_wasm.html)  
14. DuckDB-Wasm Examples \- GitHub, accessed September 16, 2025, [https://github.com/duckdb-wasm-examples](https://github.com/duckdb-wasm-examples)  
15. This looks very interesting to me, I'm building a BI reporting tool in my compan... | Hacker News, accessed September 16, 2025, [https://news.ycombinator.com/item?id=39395495](https://news.ycombinator.com/item?id=39395495)  
16. D3 by Observable | The JavaScript library for bespoke data visualization, accessed September 16, 2025, [https://d3js.org/](https://d3js.org/)  
17. What is D3? | D3 by Observable \- D3.js, accessed September 16, 2025, [https://d3js.org/what-is-d3](https://d3js.org/what-is-d3)  
18. Creating Interactive Charts with D3.js \- DEV Community, accessed September 16, 2025, [https://dev.to/ayka\_code/creating-interactive-charts-with-d3js-152o](https://dev.to/ayka_code/creating-interactive-charts-with-d3js-152o)  
19. Next.js and D3.js: Building Interactive Charts | by @rnab \- Medium, accessed September 16, 2025, [https://arnab-k.medium.com/next-js-and-d3-js-building-interactive-charts-bf99ca4979d9](https://arnab-k.medium.com/next-js-and-d3-js-building-interactive-charts-bf99ca4979d9)  
20. Building a Dynamic Data Visualization Platform with D3.js and Next.js | by @rnab \- Medium, accessed September 16, 2025, [https://arnab-k.medium.com/building-a-dynamic-data-visualization-platform-with-d3-js-and-next-js-6b6c6aae68c9](https://arnab-k.medium.com/building-a-dynamic-data-visualization-platform-with-d3-js-and-next-js-6b6c6aae68c9)  
21. Deploy to GitHub Pages \- Simply Static Documentation, accessed September 16, 2025, [https://docs.simplystatic.com/article/39-deploy-to-github-pages](https://docs.simplystatic.com/article/39-deploy-to-github-pages)  
22. Eleventy and Github pages | Léa Tortay, accessed September 16, 2025, [https://lea-tortay.com/articles/github-pages-eleventy/](https://lea-tortay.com/articles/github-pages-eleventy/)  
23. Best Practices for Building Single Page Applications (SPAs) \- PixelFreeStudio Blog, accessed September 16, 2025, [https://blog.pixelfreestudio.com/best-practices-for-building-single-page-applications-spas/](https://blog.pixelfreestudio.com/best-practices-for-building-single-page-applications-spas/)  
24. rafgraph/spa-github-pages: Host single page apps with ... \- GitHub, accessed September 16, 2025, [https://github.com/rafgraph/spa-github-pages](https://github.com/rafgraph/spa-github-pages)  
25. My page comes out 404 with routing · community · Discussion \#36908 \- GitHub, accessed September 16, 2025, [https://github.com/orgs/community/discussions/36908](https://github.com/orgs/community/discussions/36908)  
26. What is GItHub Actions? \- Harness, accessed September 16, 2025, [https://www.harness.io/blog/github-actions](https://www.harness.io/blog/github-actions)  
27. GitHub's plans, accessed September 16, 2025, [https://docs.github.com/get-started/learning-about-github/githubs-products](https://docs.github.com/get-started/learning-about-github/githubs-products)  
28. Self-hosted runners \- GitHub Docs, accessed September 16, 2025, [https://docs.github.com/actions/hosting-your-own-runners](https://docs.github.com/actions/hosting-your-own-runners)  
29. Adding self-hosted runners \- GitHub Docs, accessed September 16, 2025, [https://docs.github.com/actions/hosting-your-own-runners/managing-self-hosted-runners/adding-self-hosted-runners](https://docs.github.com/actions/hosting-your-own-runners/managing-self-hosted-runners/adding-self-hosted-runners)  
30. CircleCI's self-hosted runner overview, accessed September 16, 2025, [https://circleci.com/docs/guides/execution-runner/runner-overview/](https://circleci.com/docs/guides/execution-runner/runner-overview/)  
31. Creating Your First CI/CD Pipeline Using GitHub Actions | by Brandon Kindred \- Medium, accessed September 16, 2025, [https://brandonkindred.medium.com/creating-your-first-ci-cd-pipeline-using-github-actions-81c668008582](https://brandonkindred.medium.com/creating-your-first-ci-cd-pipeline-using-github-actions-81c668008582)  
32. Automate the Deployment of a Static Website to an S3 Bucket Using GitHub Actions, accessed September 16, 2025, [https://blogs.perficient.com/2025/03/05/automate-the-deployment-of-a-static-website-to-an-s3-bucket-using-github-actions/](https://blogs.perficient.com/2025/03/05/automate-the-deployment-of-a-static-website-to-an-s3-bucket-using-github-actions/)  
33. Deploying a Static Site \- Vite, accessed September 16, 2025, [https://vite.dev/guide/static-deploy](https://vite.dev/guide/static-deploy)