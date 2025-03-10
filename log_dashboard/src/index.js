import React from 'react';
import ReactDOM from 'react-dom/client';
import { Provider } from 'react-redux';
import { ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import App from './App';
import store from './app/store';
import { defaultTheme } from './themes';
import ErrorBoundary from './components/ErrorBoundary';

const root = ReactDOM.createRoot(document.getElementById('root'));

root.render(
    <Provider store={store}>
        <ThemeProvider theme={defaultTheme}>
            <CssBaseline />
            <ErrorBoundary>
                <App />
            </ErrorBoundary>
        </ThemeProvider>
    </Provider>
);
