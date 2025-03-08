import { configureStore } from '@reduxjs/toolkit';
import logsReducer from '../features/logs/logsSlice';

const store = configureStore({
    reducer: {
        logs: logsReducer,
    },
});

export default store;
