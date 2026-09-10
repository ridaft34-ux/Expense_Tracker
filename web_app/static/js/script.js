const searchInput = document.getElementById("searchInput");
const categoryFilter = document.getElementById("categoryFilter");


function filterExpenses() {

    const searchText =
        searchInput.value.toLowerCase().trim();

    const selectedCategory =
        categoryFilter.value;

    const rows =
        document.querySelectorAll("#expenseTable tbody tr");


    rows.forEach(row => {

        const category =
            row.cells[2]?.textContent
                .toLowerCase()
                .trim();

        const description =
            row.cells[3]?.textContent
                .toLowerCase()
                .trim();


        const matchesSearch =
            category.includes(searchText) ||
            description.includes(searchText);


        const matchesCategory =
            selectedCategory === "All" ||
            category === selectedCategory.toLowerCase();


        if (matchesSearch && matchesCategory) {

            row.style.display = "";

        } else {

            row.style.display = "none";

        }

    });
}


function clearFilters() {

    searchInput.value = "";

    categoryFilter.value = "All";

    filterExpenses();
}


searchInput.addEventListener(
    "input",
    filterExpenses
);


categoryFilter.addEventListener(
    "change",
    filterExpenses
);