function change_date(dateString) {
    return new Date(dateString).toLocaleString(undefined, {
        timeZone: Intl.DateTimeFormat().resolvedOptions().timeZone,
        hour12: true
    });
}