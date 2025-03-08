export const fetchLogsApi = async (alertId) => {
    try {
        const response = await fetch(process.env.REACT_APP_LOG_API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ alert_id: alertId }),
        });
        return await response.json();
    } catch (error) {
        console.error('Error fetching logs', error);
        throw error;
    }
};
