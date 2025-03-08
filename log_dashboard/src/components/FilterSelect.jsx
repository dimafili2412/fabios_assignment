import React from 'react';
import PropTypes from 'prop-types';
import Select from 'react-select';
import { useTheme } from '@mui/material/styles';

const FilterSelect = ({ options, value, onChange, placeholder }) => {
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

    return <Select options={options} value={value} onChange={onChange} isClearable placeholder={placeholder} styles={customStyles} />;
};

FilterSelect.propTypes = {
    options: PropTypes.array.isRequired,
    value: PropTypes.object,
    onChange: PropTypes.func.isRequired,
    placeholder: PropTypes.string,
};

FilterSelect.defaultProps = {
    placeholder: 'Select...',
};

export default FilterSelect;
