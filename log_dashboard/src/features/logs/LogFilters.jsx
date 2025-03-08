import React from 'react';
import PropTypes from 'prop-types';
import { Box } from '@mui/material';
import FilterSelect from '../../components/FilterSelect';

const LogFilters = ({ filters, eventOptions, userOptions, ipOptions, onFilterChange }) => {
    const handleEventChange = (selectedOption) => {
        onFilterChange({
            ...filters,
            eventName: selectedOption ? selectedOption.value : '',
        });
    };

    const handleUserChange = (selectedOption) => {
        onFilterChange({
            ...filters,
            userName: selectedOption ? selectedOption.value : '',
        });
    };

    const handleIpChange = (selectedOption) => {
        onFilterChange({
            ...filters,
            sourceIp: selectedOption ? selectedOption.value : '',
        });
    };

    const eventValue = eventOptions.find((opt) => opt.value === filters.eventName) || null;
    const userValue = userOptions.find((opt) => opt.value === filters.userName) || null;
    const ipValue = ipOptions.find((opt) => opt.value === filters.sourceIp) || null;

    return (
        <Box
            sx={{
                display: 'grid',
                gridTemplateColumns: { xs: '1fr', sm: '1fr 1fr 1fr' },
                gap: 2,
            }}
        >
            <FilterSelect options={eventOptions} value={eventValue} onChange={handleEventChange} placeholder="Filter by event name" />
            <FilterSelect options={userOptions} value={userValue} onChange={handleUserChange} placeholder="Filter by user name" />
            <FilterSelect options={ipOptions} value={ipValue} onChange={handleIpChange} placeholder="Filter by source IP" />
        </Box>
    );
};

LogFilters.propTypes = {
    filters: PropTypes.shape({
        eventName: PropTypes.string,
        userName: PropTypes.string,
        sourceIp: PropTypes.string,
    }).isRequired,
    eventOptions: PropTypes.array.isRequired,
    userOptions: PropTypes.array.isRequired,
    ipOptions: PropTypes.array.isRequired,
    onFilterChange: PropTypes.func.isRequired,
};

export default LogFilters;
