import { createTheme } from '@mui/material/styles';

export const defaultTheme = createTheme({
    palette: {
        primary: {
            main: '#1976d2',
        },
    },
    typography: {
        fontFamily: 'Roboto, sans-serif',
        fontSize: 14,
        fontWeightBold: 700,
    },
    spacing: 8,
    shape: {
        borderRadius: 4,
    },
    zIndex: {
        modal: 1300,
    },
});
