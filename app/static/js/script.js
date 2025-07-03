const eventsContainer = document.getElementById('events-container');

function formatDate(timestamp) {
    const date = new Date(timestamp);
    const options = {
        day: 'numeric',
        month: 'long',
        year: 'numeric',
        hour: 'numeric',
        minute: '2-digit',
        hour12: true,
        timeZone: 'UTC'
    };
    
    const formatted = date.toLocaleString('en-US', options);
    return formatted.replace(',', ' -') + ' UTC';
}

function getOrdinalSuffix(day) {
    if (day > 3 && day < 21) return 'th';
    switch (day % 10) {
        case 1: return 'st';
        case 2: return 'nd';
        case 3: return 'rd';
        default: return 'th';
    }
}

function formatEventText(event) {
    const date = new Date(event.timestamp);
    const day = date.getUTCDate();
    const formattedDate = formatDate(event.timestamp).replace(
        day.toString(),
        day + getOrdinalSuffix(day)
    );
    
    let text = '';
    
    switch (event.action) {
        case 'PUSH':
            text = `<span class="event-author">"${event.author}"</span> pushed to <span class="event-branch">"${event.to_branch}"</span> on ${formattedDate}`;
            break;
        case 'PULL_REQUEST':
            text = `<span class="event-author">"${event.author}"</span> submitted a pull request from <span class="event-branch">"${event.from_branch}"</span> to <span class="event-branch">"${event.to_branch}"</span> on ${formattedDate}`;
            break;
        case 'MERGE':
            text = `<span class="event-author">"${event.author}"</span> merged branch <span class="event-branch">"${event.from_branch}"</span> to <span class="event-branch">"${event.to_branch}"</span> on ${formattedDate}`;
            break;
    }
    
    return text;
}

function renderEvents(events) {
    if (events.length === 0) {
        eventsContainer.innerHTML = '<div class="loading">No events yet...</div>';
        return;
    }
    
    const html = events.map(event => `
        <div class="event-item event-${event.action.toLowerCase()}">
            <div class="event-text">${formatEventText(event)}</div>
        </div>
    `).join('');
    
    eventsContainer.innerHTML = html;
}

async function fetchEvents() {
    try {
        const response = await fetch('/api/events');
        if (!response.ok) throw new Error('Failed to fetch events');
        
        const events = await response.json();
        renderEvents(events);
    } catch (error) {
        console.error('Error fetching events:', error);
        eventsContainer.innerHTML = '<div class="error">Error loading events. Please try again later.</div>';
    }
}

// Initial fetch
fetchEvents();

// Poll every 15 seconds
setInterval(fetchEvents, 15000);