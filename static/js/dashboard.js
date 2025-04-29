/**
 * Customer Review Insights - Dashboard Scripts
 * Handles interactive elements and additional features for the dashboard
 */

document.addEventListener('DOMContentLoaded', function() {
    // Add event listeners to dashboard elements
    addTabularViewListener();
    addFilterListeners();
    addSortListeners();
    addExportListener();
    
    // Add responsiveness to charts
    handleChartResize();
});

/**
 * Add event listener for tabular view of data
 */
function addTabularViewListener() {
    const tabularViewBtn = document.getElementById('show-tabular-view');
    if (!tabularViewBtn) return;
    
    tabularViewBtn.addEventListener('click', function() {
        const dataContainer = document.getElementById('tabular-data-container');
        if (!dataContainer) return;
        
        if (dataContainer.classList.contains('d-none')) {
            // Show loading indicator
            dataContainer.innerHTML = '<div class="text-center py-5"><div class="spinner-border text-primary" role="status"></div><p class="mt-2">Loading data...</p></div>';
            dataContainer.classList.remove('d-none');
            
            // Fetch the data from the API
            fetch(window.location.href.replace('dashboard', 'api/data'))
                .then(response => response.json())
                .then(data => {
                    renderTabularView(data, dataContainer);
                })
                .catch(error => {
                    dataContainer.innerHTML = `<div class="alert alert-danger">Error loading data: ${error.message}</div>`;
                });
        } else {
            dataContainer.classList.add('d-none');
        }
    });
}

/**
 * Render tabular view of the data
 */
function renderTabularView(data, container) {
    if (!data || !data.length) {
        container.innerHTML = '<div class="alert alert-info">No data available</div>';
        return;
    }
    
    // Create table structure
    let tableHtml = `
        <div class="table-responsive">
            <table class="table table-striped table-hover">
                <thead class="table-dark">
                    <tr>
                        <th>ID</th>
                        <th>Original Review</th>
                        <th>Language</th>
                        <th>Translated (if needed)</th>
                        <th>Sentiment</th>
                        <th>Score</th>
                    </tr>
                </thead>
                <tbody>
    `;
    
    // Add table rows
    data.forEach(row => {
        // Determine if translation was needed
        const wasTranslated = row.is_english ? '' : `
            <div class="translated-text">
                ${row.review_text}
            </div>
        `;
        
        // Determine sentiment class
        let sentimentClass = '';
        if (row.sentiment === 'positive') sentimentClass = 'text-success';
        else if (row.sentiment === 'negative') sentimentClass = 'text-danger';
        
        tableHtml += `
            <tr>
                <td>${row.review_id}</td>
                <td>${row.original_review.length > 100 ? row.original_review.substring(0, 100) + '...' : row.original_review}</td>
                <td>${row.language}</td>
                <td>${row.is_english ? 'N/A' : (row.review_text.length > 100 ? row.review_text.substring(0, 100) + '...' : row.review_text)}</td>
                <td class="${sentimentClass}">${row.sentiment}</td>
                <td>${row.sentiment_score.toFixed(2)}</td>
            </tr>
        `;
    });
    
    tableHtml += `
                </tbody>
            </table>
        </div>
    `;
    
    container.innerHTML = tableHtml;
}

/**
 * Add event listeners for filtering the data
 */
function addFilterListeners() {
    const filterButtons = document.querySelectorAll('[data-filter]');
    if (!filterButtons.length) return;
    
    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            const filterType = this.getAttribute('data-filter');
            
            // Update active button
            filterButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            
            // Apply filter (would need to be implemented depending on your data structure)
            console.log(`Filter by: ${filterType}`);
            
            // In a real implementation, you would filter the data and update charts
        });
    });
}

/**
 * Add event listeners for sorting the data
 */
function addSortListeners() {
    const sortSelects = document.querySelectorAll('[data-sort]');
    if (!sortSelects.length) return;
    
    sortSelects.forEach(select => {
        select.addEventListener('change', function() {
            const sortType = this.value;
            
            // In a real implementation, you would sort the data and update charts
            console.log(`Sort by: ${sortType}`);
        });
    });
}

/**
 * Add event listener for exporting data
 */
function addExportListener() {
    const exportBtn = document.getElementById('export-data');
    if (!exportBtn) return;
    
    exportBtn.addEventListener('click', function() {
        // Fetch data and export to CSV
        fetch(window.location.href.replace('dashboard', 'api/data'))
            .then(response => response.json())
            .then(data => {
                exportToCSV(data, 'review_analysis.csv');
            })
            .catch(error => {
                alert(`Error exporting data: ${error.message}`);
            });
    });
}

/**
 * Export data to CSV file
 */
function exportToCSV(data, filename) {
    if (!data || !data.length) {
        alert('No data to export');
        return;
    }
    
    // Get headers
    const headers = Object.keys(data[0]);
    
    // Format CSV rows
    const rows = [
        headers.join(','),
        ...data.map(row => headers.map(header => {
            // Handle commas and quotes in data
            let cell = row[header] || '';
            if (typeof cell === 'string' && (cell.includes(',') || cell.includes('"'))) {
                cell = `"${cell.replace(/"/g, '""')}"`;
            }
            return cell;
        }).join(','))
    ];
    
    // Create CSV content
    const csvContent = rows.join('\n');
    
    // Create download link
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    
    link.setAttribute('href', url);
    link.setAttribute('download', filename);
    link.style.visibility = 'hidden';
    
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

/**
 * Handle chart resizing when window size changes
 */
function handleChartResize() {
    const charts = [
        'sentiment-pie-chart',
        'language-pie-chart',
        'sentiment-histogram',
        'sentiment-by-language'
    ];
    
    window.addEventListener('resize', function() {
        charts.forEach(chartId => {
            const chartElement = document.getElementById(chartId);
            if (chartElement && window.Plotly) {
                Plotly.relayout(chartId, {
                    'width': chartElement.offsetWidth
                });
            }
        });
    });
}