// Filter Businesses by Category
function filterCategory(category) {
    $('.business').each(function () {
        $(this).toggle(category === 'All' || $(this).data('category').toLowerCase() === category.toLowerCase());
    });
}

// Filter Businesses by Location
function filterLocation(location) {
    $('.business').each(function () {
        let businessLocation = $(this).data('location');
        $(this).toggle(location === 'All' || businessLocation.toLowerCase() === location.toLowerCase());
    });
}

// Search Businesses
function searchBusinesses() {
    let query = $('#searchBox').val().toLowerCase();
    $('.business').each(function () {
        let name = $(this).find('h5').text().toLowerCase();
        $(this).toggle(name.includes(query));
    });
}

// Sort Businesses
function sortBusinesses(criteria) {
    let businessList = $('#businessList');
    let businesses = $('.business').toArray().sort((a, b) => {
        let aValue = $(a).find('h5').text().toLowerCase();
        let bValue = $(b).find('h5').text().toLowerCase();
        if (criteria === 'category') {
            aValue = $(a).data('category').toLowerCase();
            bValue = $(b).data('category').toLowerCase();
        }
        return aValue.localeCompare(bValue);
    });
    businessList.append(businesses);
}

$("#state").change(function () {
    const stateId = $(this).val(); // Get the selected state ID
    const lgaSelect = $("#lga"); // Reference the LGA dropdown

    // Clear existing LGA options
    lgaSelect.empty();

    // Fetch LGAs for the selected state
    $.ajax({
        url: `/get_lgas/${stateId}`,
        method: "GET",
        success: function (data) {
            // Populate the LGA dropdown with the fetched data
            data.lgas.forEach(function (lga) {
                lgaSelect.append(new Option(lga.name, lga.id));
            });
        },
        error: function () {
            alert("Failed to fetch LGAs. Please try again.");
        },
    });
});

// Initialize Google Maps
function initMap() {
    try {
        const defaultLocation = { lat: 6.5244, lng: 3.3792 }; // Default to Lagos
        const mapElement = $("#map")[0];

        // Initialize the map
        const map = new google.maps.Map(mapElement, {
            center: defaultLocation,
            zoom: 13,
        });

        // Initialize the marker
        const marker = new google.maps.Marker({
            position: defaultLocation,
            map: map,
            draggable: true,
        });

        // Update latitude and longitude when marker is dragged
        google.maps.event.addListener(marker, "dragend", function () {
            const position = marker.getPosition();
            $("#latitude").val(position.lat());
            $("#longitude").val(position.lng());
        });

        // Initialize the search box
        const input = $("#locationSearch")[0];
        const searchBox = new google.maps.places.SearchBox(input);

        // Bias the search box results towards the map's viewport
        map.addListener("bounds_changed", function () {
            searchBox.setBounds(map.getBounds());
        });

        // Listen for the event when a place is selected
        searchBox.addListener("places_changed", function () {
            const places = searchBox.getPlaces();
            if (places.length === 0) {
                console.error("No places found.");
                return;
            }

            const place = places[0];
            if (!place.geometry || !place.geometry.location) {
                console.error("Invalid place geometry.");
                return;
            }

            // Update the map and marker position
            map.setCenter(place.geometry.location);
            marker.setPosition(place.geometry.location);

            // Update the latitude and longitude fields
            $("#latitude").val(place.geometry.location.lat());
            $("#longitude").val(place.geometry.location.lng());
        });
    } catch (error) {
        console.error("Error initializing map:", error);
    }
}

// Show Alerts
function showAlert(message, type) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;

    const container = document.querySelector('.container-fluid');
    container.insertBefore(alertDiv, container.firstChild);

    // Auto dismiss after 5 seconds
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}

// Handle Tab Switching for Login/Register
$("#loginTab").click(function () {
    $("#loginForm").show();
    $("#registerForm").hide();
    $("#loginTab").addClass("active");
    $("#registerTab").removeClass("active");
});

$("#registerTab").click(function () {
    $("#registerForm").removeClass("d-none");
    $("#registerForm").show();
    $("#loginForm").hide();
    $("#registerTab").addClass("active");
    $("#loginTab").removeClass("active");
});

// Handle Image Preview for Business Logo
$("#businessLogo").change(function (event) {
    let file = event.target.files[0];
    if (file) {
        let reader = new FileReader();
        reader.onload = function (e) {
            $("#imagePreview").attr("src", e.target.result).fadeIn();
        };
        reader.readAsDataURL(file);
    }
});

// Document Ready
$(document).ready(function () {
    // Initialize Google Maps if the map element exists
    if ($("#map").length) {
        initMap();
    }
    
    
    // Add default options to dropdowns
    $(".register_state").prepend('<option value="" disabled selected>Select a State</option>');
    $(".register_lga").prepend('<option value="" disabled selected>Select an LGA</option>');
    $(".register_category").prepend('<option value="" disabled selected>Select a Category</option>');
});

function showAlert(message, type) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    const container = document.querySelector('.container-fluid');
    container.insertBefore(alertDiv, container.firstChild);
    
    // Auto dismiss after 5 seconds
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}

function updateStatistics() {
    // Update total businesses count
    const totalBusinessesElement = document.querySelector('[data-stat="total-businesses"]');
    if (totalBusinessesElement) {
        const currentCount = parseInt(totalBusinessesElement.textContent);
        totalBusinessesElement.textContent = currentCount - 1;
    }
    
    // You might want to refresh the page if the statistics are complex
    if (document.querySelectorAll('tr[data-business-id]').length === 0) {
        location.reload();
    }
}

function confirmDelete() {
    if (confirm('Are you sure you want to delete your account? This will also delete all your businesses and reviews. This action cannot be undone.')) {
        fetch('/delete_profile', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('input[name="csrf_token"]').value
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(data.message);
                window.location.href = '/login';
            } else {
                alert(data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while deleting your account');
        });
    }
}


function deleteBusiness(businessId, businessName) {
    if (confirm(`Are you sure you want to delete ${businessName}? This action cannot be undone.`)) {
        fetch(`/admin/delete_business/${businessId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload();
            } else {
                alert(data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while deleting the business');
        });
    }
}

function userDeleteBusiness(businessId, businessName) {
    if (confirm(`Are you sure you want to delete ${businessName}? This action cannot be undone.`)) {
        fetch(`/delete_business/${businessId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload();
            } else {
                alert(data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while deleting the business');
        });
    }
}

function deleteReview(reviewId) {
    if (confirm('Are you sure you want to delete this review?')) {
        fetch(`/admin/delete_review/${reviewId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': '{{ csrf_token() }}'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload();
            } else {
                alert(data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while deleting the review');
        });
    }
}

function banUser(userId, userName) {
    if (confirm(`Are you sure you want to ban ${userName}? This will delete all their businesses and reviews.`)) {
        fetch(`/admin/ban_user/${userId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': '{{ csrf_token() }}'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload();
            } else {
                alert(data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while banning the user');
        });
    }
}

function deleteReport(reportId) {
    if (confirm("Are you sure you want to delete this report?")) {
        fetch(`/admin/reports/delete/${reportId}`, {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json",
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(data.message);
                location.reload();
            } else {
                alert(data.message);
            }
        })
        .catch(error => {
            console.error("Error:", error);
            alert("An error occurred while deleting the report.");
        });
    }
}

function showReportModal(reportType, reportId) {
    // Set the hidden fields in the report modal
    $("#reportTypeField").val(reportType);
    $("#reportIdField").val(reportId);

    // Show the modal
    $("#reportModal").modal("show");
}