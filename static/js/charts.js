document.addEventListener('DOMContentLoaded', function() {
    // Only initialize charts if we're on the dashboard page
    const dashboardCharts = document.getElementById('dashboardCharts');
    if (!dashboardCharts) return;
    
    // Device Status Distribution Chart
    const statusChartElement = document.getElementById('deviceStatusChart');
    if (statusChartElement) {
        // Get data from data attributes
        const workingDevices = parseInt(statusChartElement.dataset.working || 0);
        const faultyDevices = parseInt(statusChartElement.dataset.faulty || 0);
        const maintenanceDevices = parseInt(statusChartElement.dataset.maintenance || 0);
        const outOfServiceDevices = parseInt(statusChartElement.dataset.outOfService || 0);
        
        const statusChart = new Chart(statusChartElement, {
            type: 'doughnut',
            data: {
                labels: ['Working', 'Faulty', 'Under Maintenance', 'Out of Service'],
                datasets: [{
                    data: [workingDevices, faultyDevices, maintenanceDevices, outOfServiceDevices],
                    backgroundColor: ['#28a745', '#dc3545', '#ffc107', '#6c757d'],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom'
                    },
                    title: {
                        display: true,
                        text: 'Device Status Distribution'
                    }
                }
            }
        });
    }
    
    // Device Category Distribution Chart
    const categoryChartElement = document.getElementById('deviceCategoryChart');
    if (categoryChartElement) {
        // Parse data from data-categories attribute (JSON string)
        const categoriesJson = categoryChartElement.dataset.categories || '[]';
        const categories = JSON.parse(categoriesJson);
        
        const labels = categories.map(c => c.category);
        const data = categories.map(c => c.count);
        
        const categoryChart = new Chart(categoryChartElement, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Number of Devices',
                    data: data,
                    backgroundColor: '#FF9900',
                    borderColor: '#232F3E',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    title: {
                        display: true,
                        text: 'Devices by Category'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            precision: 0
                        }
                    }
                }
            }
        });
    }
    
    // Report Status Chart
    const reportChartElement = document.getElementById('reportStatusChart');
    if (reportChartElement) {
        const pendingReports = parseInt(reportChartElement.dataset.pending || 0);
        const resolvedReports = parseInt(reportChartElement.dataset.resolved || 0);
        
        const reportChart = new Chart(reportChartElement, {
            type: 'pie',
            data: {
                labels: ['Pending', 'Resolved'],
                datasets: [{
                    data: [pendingReports, resolvedReports],
                    backgroundColor: ['#17a2b8', '#28a745'],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom'
                    },
                    title: {
                        display: true,
                        text: 'Report Status Distribution'
                    }
                }
            }
        });
    }
    
    // Monthly Fault Reports Chart
    const monthlyReportsElement = document.getElementById('monthlyReportsChart');
    if (monthlyReportsElement) {
        // Parse data from data-reports attribute (JSON string)
        const reportsJson = monthlyReportsElement.dataset.reports || '[]';
        const monthlyData = JSON.parse(reportsJson);
        
        const months = monthlyData.map(d => d.month);
        const counts = monthlyData.map(d => d.count);
        
        const monthlyChart = new Chart(monthlyReportsElement, {
            type: 'line',
            data: {
                labels: months,
                datasets: [{
                    label: 'Fault Reports',
                    data: counts,
                    fill: false,
                    borderColor: '#FF9900',
                    tension: 0.1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: 'Monthly Fault Reports'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            precision: 0
                        }
                    }
                }
            }
        });
    }
});
