import React from 'react';
import PropTypes from 'prop-types';
import DataTable from '../../components/DataTable';

const LogTable = ({ logs }) => {
    const columns = [
        { header: 'Timestamp', field: 'timestamp' },
        { header: 'Event Name', field: 'event_name' },
        {
            header: 'User Name',
            field: 'user_identity',
            renderCell: (row) => row.user_identity?.userName || '',
        },
        { header: 'Source IP', field: 'source_ip' },
    ];

    return <DataTable columns={columns} data={logs} />;
};

LogTable.propTypes = {
    logs: PropTypes.arrayOf(
        PropTypes.shape({
            timestamp: PropTypes.string.isRequired,
            event_name: PropTypes.string.isRequired,
            source_ip: PropTypes.string.isRequired,
            user_identity: PropTypes.shape({
                userName: PropTypes.string,
            }),
        })
    ).isRequired,
};

export default LogTable;
