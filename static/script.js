const dateFormatOptions = { weekday: 'short', day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit' };
const dateFormatLocation = 'en-GB';

function fromToDateFormat(startDateTime, endDateTime) {
    return new Date(startDateTime).toLocaleString(dateFormatLocation, dateFormatOptions) + ' - ' + new Date(endDateTime).toLocaleString(dateFormatLocation, { hour: '2-digit', minute: '2-digit' });
}