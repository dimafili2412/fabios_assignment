import React from 'react';
import PropTypes from 'prop-types';
import Select from 'react-select';
import { Box } from '@mui/material';
import { useTheme } from '@mui/material/styles';

const alertOptions = [
    { value: 'ALERT1', label: 'ALERT1' },
    { value: 'ALERT2', label: 'ALERT2' },
    { value: 'ALERT3', label: 'ALERT3' },
    { value: 'ALERT4', label: 'ALERT4' },
];

const AlertSelector = ({ onChange }) => {
    const theme = useTheme();

    const customStyles = {
        control: (provided) => ({
            ...provided,
            minHeight: theme.spacing(7),
            fontSize: theme.typography.fontSize,
        }),
        menu: (provided) => ({
            ...provided,
            zIndex: theme.zIndex.modal + 1,
        }),
    };

    return (
        <Box>
            <Select options={alertOptions} onChange={onChange} isClearable placeholder="Select an alert..." styles={customStyles} />
        </Box>
    );
};

AlertSelector.propTypes = {
    onChange: PropTypes.func.isRequired,
};

export default AlertSelector;
