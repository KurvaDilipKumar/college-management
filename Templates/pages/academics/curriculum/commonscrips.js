document.addEventListener("DOMContentLoaded", function () {
  // Main filter buttons (B.Tech, M.Tech, etc.)
  const mainFilters = document.querySelectorAll(".filter-btn[data-group]");
  const subFilters = document.querySelectorAll(".filter-btn[data-subgroup]");

  // Function to handle main filter selection
  function handleMainFilter(group) {
    // Hide all group contents and remove active class from main filters
    document.querySelectorAll(".group-content").forEach((content) => {
      content.classList.remove("active");
    });
    mainFilters.forEach((btn) => btn.classList.remove("active"));

    // Show selected group content and add active class
    const selectedGroup = document.querySelector(
      `.group-content[data-group="${group}"]`
    );
    if (selectedGroup) {
      selectedGroup.classList.add("active");
      const clickedBtn = document.querySelector(
        `.filter-btn[data-group="${group}"]`
      );
      clickedBtn.classList.add("active");

      // Reset all sub-filters in this group
      const subFilterButtons = selectedGroup.querySelectorAll(
        ".filter-btn[data-subgroup]"
      );
      const subGroups = selectedGroup.querySelectorAll(".sub-group");
      subFilterButtons.forEach((btn) => btn.classList.remove("active"));
      subGroups.forEach((sub) => sub.classList.remove("active"));

      // Activate first sub-filter if exists
      const firstSubFilter = selectedGroup.querySelector(
        ".filter-btn[data-subgroup]"
      );
      if (firstSubFilter) {
        firstSubFilter.classList.add("active");
        const firstSubGroup = selectedGroup.querySelector(
          `.sub-group[data-subgroup="${firstSubFilter.dataset.subgroup}"]`
        );
        if (firstSubGroup) {
          firstSubGroup.classList.add("active");
        }
      }
    }
  }

  // Function to handle sub-filter selection
  function handleSubFilter(subgroup, parentGroup) {
    if (!parentGroup) return;

    // Remove active class from all sub-filters and sub-groups in this parent group
    const subFilterButtons = parentGroup.querySelectorAll(
      ".filter-btn[data-subgroup]"
    );
    const subGroups = parentGroup.querySelectorAll(".sub-group");
    subFilterButtons.forEach((btn) => btn.classList.remove("active"));
    subGroups.forEach((sub) => sub.classList.remove("active"));

    // Add active class to clicked sub-filter and show corresponding sub-group
    const clickedSubFilter = parentGroup.querySelector(
      `.filter-btn[data-subgroup="${subgroup}"]`
    );
    const selectedSubGroup = parentGroup.querySelector(
      `.sub-group[data-subgroup="${subgroup}"]`
    );
    if (clickedSubFilter) {
      clickedSubFilter.classList.add("active");
    }
    if (selectedSubGroup) {
      selectedSubGroup.classList.add("active");
    }
  }

  // Main filter click handler
  mainFilters.forEach((btn) => {
    btn.addEventListener("click", function () {
      handleMainFilter(this.dataset.group);
    });
  });

  // Sub-filter click handler
  subFilters.forEach((btn) => {
    btn.addEventListener("click", function () {
      const parentGroup = this.closest(".group-content");
      handleSubFilter(this.dataset.subgroup, parentGroup);
    });
  });

  // Initialize with B.Tech section active
  const initialMainFilter = document.querySelector(
    '.filter-btn[data-group="btech"]'
  );
  if (initialMainFilter) {
    handleMainFilter("btech");
  }
});
