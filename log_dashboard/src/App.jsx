import React, { useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { Container, AppBar, Toolbar, Typography, Box, Paper, CircularProgress, Alert } from '@mui/material';
import { useTheme } from '@mui/material/styles';
import AlertSelector from './features/logs/AlertSelector';
import LogTable from './features/logs/LogTable';
import LogFilters from './features/logs/LogFilters';
import {
    setSelectedAlert,
    setFilters,
    fetchLogs,
    selectFilteredLogs,
    selectEventOptions,
    selectUserOptions,
    selectIpOptions,
} from './features/logs/logsSlice';

const App = () => {
    const dispatch = useDispatch();
    const theme = useTheme();
    const { selectedAlert, alertName, loading, error } = useSelector((state) => state.logs);

    const filteredLogs = useSelector(selectFilteredLogs);
    const eventOptions = useSelector(selectEventOptions);
    const userOptions = useSelector(selectUserOptions);
    const ipOptions = useSelector(selectIpOptions);

    // Fetch logs when a new alert is selected
    useEffect(() => {
        if (selectedAlert) {
            dispatch(fetchLogs(selectedAlert.value));
        }
    }, [selectedAlert, dispatch]);

    // Handlers for alert and filter changes
    const handleAlertChange = (option) => {
        dispatch(setSelectedAlert(option || null));
    };

    const handleFilterChange = (updatedFilters) => {
        dispatch(setFilters(updatedFilters));
    };

    return (
        <Container>
            <AppBar position="static" sx={{ mb: theme.spacing(4) }}>
                <Toolbar sx={{ display: 'flex', justifyContent: 'center' }}>
                    <Typography variant="h4">Alert Log Dashboard</Typography>
                </Toolbar>
            </AppBar>

            <Paper sx={{ p: theme.spacing(3), mb: theme.spacing(3) }}>
                <AlertSelector onChange={handleAlertChange} />
            </Paper>

            <Paper sx={{ p: theme.spacing(3), mb: theme.spacing(3) }}>
                <LogFilters
                    filters={useSelector((state) => state.logs.filters)}
                    eventOptions={eventOptions}
                    userOptions={userOptions}
                    ipOptions={ipOptions}
                    onFilterChange={handleFilterChange}
                />
            </Paper>

            <Paper sx={{ p: theme.spacing(3) }}>
                {alertName && (
                    <Typography variant="h5" sx={{ mb: theme.spacing(2) }}>
                        {alertName}
                    </Typography>
                )}
                {loading ? (
                    <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: theme.spacing(25) }}>
                        <CircularProgress />
                    </Box>
                ) : error ? (
                    <Alert severity="error">Error: {error}</Alert>
                ) : (
                    <LogTable logs={filteredLogs} />
                )}
            </Paper>
        </Container>
    );
};

export default App;
