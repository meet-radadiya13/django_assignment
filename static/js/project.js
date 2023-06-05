function change_date(dateString) {
    // let utc_date = new Date(dateString);
    // let date = new Date(utc_date.setMinutes(utc_date.getMinutes() + utc_date.getTimezoneOffset()))
    // local = date.toLocaleString('en-US', {hour12: true})
    // return local[1] + " " + local[2] + " " + local[3] + ", " + local[4];
    return new Date(dateString).toLocaleString(undefined, {
        timeZone: Intl.DateTimeFormat().resolvedOptions().timeZone,
        hour12: true
    });
}