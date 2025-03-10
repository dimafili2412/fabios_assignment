# Fabios assignment - Log Dashboard

Fetches logs from an api and displays them in a table with filtering options.
Use npm start to run the app and build to compile and serve the app.
In case of getting cors errors in testing run Chrome with the following flags: --disable-web-security --user-data-dir=%LOCALAPPDATA%\Google\chromeTemp

.env required, keys:

-   REACT_APP_LOG_API_URL (API endpoint for log fetching)

By Dmitry Filipovich :)

## Running The Project
Follow these steps to set up and run the project locally:

```bash
# Change into the project directory
cd log_dashboard

# Install all required dependencies
npm install

# Start the development server
npm start
```

## Available Scripts

In the project directory, you can run:

### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

The page will reload when you make changes.\
You may also see any lint errors in the console.

### `npm test`

Launches the test runner in the interactive watch mode.\
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

### `npm run build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

### `npm run eject`

**Note: this is a one-way operation. Once you `eject`, you can't go back!**

If you aren't satisfied with the build tool and configuration choices, you can `eject` at any time. This command will remove the single build dependency from your project.

Instead, it will copy all the configuration files and the transitive dependencies (webpack, Babel, ESLint, etc) right into your project so you have full control over them. All of the commands except `eject` will still work, but they will point to the copied scripts so you can tweak them. At this point you're on your own.

You don't have to ever use `eject`. The curated feature set is suitable for small and middle deployments, and you shouldn't feel obligated to use this feature. However we understand that this tool wouldn't be useful if you couldn't customize it when you are ready for it.

# Fabios assignment - Log Aggregator

Aggregates logs from a log files.
Provides the following metrics:

-   Requests Per Hour
-   Most Requested Resources
-   Response Code Distribution
-   Anomalies (Request frequency and error count)

To run install Python 3.13.2 and run main.py.
No additional dependencies.

Edit the respctive config files to control both the aggregator and and generator.
