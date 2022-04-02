function deleteAccount() {
    if (confirm("WARNING! Account deletion CANNOT be reversed! All your activities pending approval will be deleted. If you are the creator of a group, that group, as well as all its activities and members, will also be erased. Are you sure you want to continue?")) {
        window.location.replace("/profile/delete")
    }
}