function deletionPrompt(activityID, csrfToken) {
    if (confirm("Are you sure you want to delete this activity? This action cannot be reversed.")) {
        window.location.replace("/activities/delete?activity=" + activityID + "&token=" + csrfToken)
    } else {
        
    }
}