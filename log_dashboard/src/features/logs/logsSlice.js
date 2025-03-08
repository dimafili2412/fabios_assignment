import { createSlice, createAsyncThunk, createSelector } from '@reduxjs/toolkit';
import { fetchLogsApi } from '../../api/logApi';

// Async thunk to fetch logs
export const fetchLogs = createAsyncThunk('logs/fetchLogs', async (alertId, { rejectWithValue }) => {
    try {
        const data = await fetchLogsApi(alertId);
        return data;
    } catch (error) {
        return rejectWithValue(error.message || 'Failed to fetch logs');
    }
});

const initialState = {
    selectedAlert: null,
    alertName: '',
    logs: [],
    filters: {
        eventName: '',
        userName: '',
        sourceIp: '',
    },
    loading: false,
    error: null,
};

const logsSlice = createSlice({
    name: 'logs',
    initialState,
    reducers: {
        setSelectedAlert(state, action) {
            state.selectedAlert = action.payload;
            // Reset logs and alert name if no alert is selected
            if (!action.payload) {
                state.logs = [];
                state.alertName = '';
            }
        },
        setFilters(state, action) {
            state.filters = { ...state.filters, ...action.payload };
        },
    },
    extraReducers: (builder) => {
        builder
            .addCase(fetchLogs.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(fetchLogs.fulfilled, (state, action) => {
                state.loading = false;
                state.alertName = action.payload.alert_name || '';
                state.logs = action.payload.cloudtrail_logs || [];
            })
            .addCase(fetchLogs.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload || action.error.message;
            });
    },
});

export const { setSelectedAlert, setFilters } = logsSlice.actions;
export default logsSlice.reducer;

/* ------------------- Selectors ------------------- */
// Base selectors
export const selectLogsState = (state) => state.logs;
export const selectLogs = (state) => state.logs.logs;
export const selectFilters = (state) => state.logs.filters;

// Selector for filtered logs.
export const selectFilteredLogs = createSelector([selectLogs, selectFilters], (logs, filters) => {
    return logs.filter((log) => {
        const matchesEvent = filters.eventName ? log.event_name.toLowerCase().includes(filters.eventName.toLowerCase()) : true;
        const matchesUser = filters.userName ? log.user_identity?.userName.toLowerCase().includes(filters.userName.toLowerCase()) : true;
        const matchesIp = filters.sourceIp ? log.source_ip.toLowerCase().includes(filters.sourceIp.toLowerCase()) : true;
        return matchesEvent && matchesUser && matchesIp;
    });
});

// Selector for event options
export const selectEventOptions = createSelector([selectLogs], (logs) => {
    const uniqueEvents = Array.from(new Set(logs.map((log) => log.event_name)));
    return uniqueEvents.map((e) => ({ value: e, label: e }));
});

// Selector for user options
export const selectUserOptions = createSelector([selectLogs], (logs) => {
    const uniqueUsers = Array.from(new Set(logs.map((log) => log.user_identity?.userName).filter(Boolean)));
    return uniqueUsers.map((u) => ({ value: u, label: u }));
});

// Selector for IP options
export const selectIpOptions = createSelector([selectLogs], (logs) => {
    const uniqueIps = Array.from(new Set(logs.map((log) => log.source_ip).filter(Boolean)));
    return uniqueIps.map((ip) => ({ value: ip, label: ip }));
});
