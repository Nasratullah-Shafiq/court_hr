///** @odoo-module **/
//
//import {
//    Component,
//    onWillStart,
//    onMounted,
//    onWillUnmount,
//    useState,
//} from "@odoo/owl";
//
//import { registry } from "@web/core/registry";
//import { useService } from "@web/core/utils/hooks";
//import { loadJS } from "@web/core/assets";
//
//
//class EmployeeDashboard extends Component {
//
//    setup() {
//        this.orm = useService("orm");
//        this.actionService = useService("action");
//
//        // =========================================================
//        // STATE
//        // =========================================================
//
//        this.state = useState({
//
//            // General
//            total_count: 0,
//            active_count: 0,
//            inactive_count: 0,
//
//            // Gender
//            male_count: 0,
//            female_count: 0,
//            other_gender_count: 0,
//
//            // Job status
//            current_count: 0,
//            separated_count: 0,
//            detached_count: 0,
//            dismissed_count: 0,
//            unknown_status_count: 0,
//            retired_count: 0,
//            deceased_count: 0,
//
//            // Category
//            administrative_count: 0,
//            service_count: 0,
//            judicial_count: 0,
//            military_count: 0,
//
//            // Related records
//            education_count: 0,
//            experience_count: 0,
//            training_count: 0,
//            retirement_count: 0,
//
//            // Filter
//            selected_year: "all",
//        });
//
//        // =========================================================
//        // CHARTS
//        // =========================================================
//
//        this.genderChart = null;
//        this.statusChart = null;
//        this.categoryChart = null;
//
//        // =========================================================
//        // INITIALIZATION
//        // =========================================================
//
//        onWillStart(async () => {
//
//            await loadJS(
//                "https://cdn.jsdelivr.net/npm/chart.js"
//            );
//
//            await this.loadData();
//        });
//
//        onMounted(() => {
//
//            this.renderGenderChart();
//            this.renderStatusChart();
//            this.renderCategoryChart();
//        });
//
//        onWillUnmount(() => {
//
//            if (this.genderChart) {
//                this.genderChart.destroy();
//            }
//
//            if (this.statusChart) {
//                this.statusChart.destroy();
//            }
//
//            if (this.categoryChart) {
//                this.categoryChart.destroy();
//            }
//        });
//    }
//
//
//    // =============================================================
//    // DOMAIN
//    // =============================================================
//
//    getEmployeeDomain() {
//
//        const domain = [];
//
//        if (this.state.selected_year !== "all") {
//
//            domain.push([
//                "recruitment_date",
//                ">=",
//                `${this.state.selected_year}-01-01`,
//            ]);
//
//            domain.push([
//                "recruitment_date",
// "<=",
//                `${this.state.selected_year}-12-31`,
//            ]);
//        }
//
//        return domain;
//    }
//
//
//    // =============================================================
//    // LOAD DATA
//    // =============================================================
//
//    async loadData() {
//
//        const domain = this.getEmployeeDomain();
//
//        // ---------------------------------------------------------
//        // GENERAL EMPLOYEE COUNTS
//        // ---------------------------------------------------------
//
//        const total_count = await this.orm.searchCount(
//            "hr.employee",
//            domain
//        );
//
//        const active_count = await this.orm.searchCount(
//            "hr.employee",
//            [
//                ...domain,
//                ["active", "=", true],
//            ]
//        );
//
//        const inactive_count = await this.orm.searchCount(
//            "hr.employee",
//            [
//                ...domain,
//                ["active", "=", false],
//            ]
//        );
//
//
//        // ---------------------------------------------------------
//        // GENDER
//        // ---------------------------------------------------------
//
//        const male_count = await this.orm.searchCount(
//            "hr.employee",
//            [
//                ...domain,
//                ["emp_gender", "=", "male"],
//            ]
//        );
//
//        const female_count = await this.orm.searchCount(
//            "hr.employee",
//            [
//                ...domain,
//                ["emp_gender", "=", "female"],
//            ]
//        );
//
//        const other_gender_count = await this.orm.searchCount(
//            "hr.employee",
//            [
//                ...domain,
//                ["emp_gender", "=", "other"],
//            ]
//        );
//
//
//        // ---------------------------------------------------------
//        // JOB STATUS
//        // ---------------------------------------------------------
//
//        const current_count = await this.orm.searchCount(
//            "hr.employee",
//            [
//                ...domain,
//                ["job_status", "=", "برحال"],
//            ]
//        );
//
//        const separated_count = await this.orm.searchCount(
//            "hr.employee",
//            [
//                ...domain,
//                ["job_status", "=", "منفصل"],
//            ]
//        );
//
//        const detached_count = await this.orm.searchCount(
//            "hr.employee",
//            [
//                ...domain,
//                ["job_status", "=", "منفک"],
//            ]
//        );
//
//        const dismissed_count = await this.orm.searchCount(
//            "hr.employee",
//            [
//                ...domain,
//                ["job_status", "=", "معزول"],
//            ]
//        );
//
//        const retired_count = await this.orm.searchCount(
//            "hr.employee",
//            [
//                ...domain,
//                ["job_status", "=", "متقاعد"],
//            ]
//        );
//
//        const deceased_count = await this.orm.searchCount(
//            "hr.employee",
//            [
//                ...domain,
//                ["job_status", "=", "وفات"],
//            ]
//        );
//
//
//        // ---------------------------------------------------------
//        // CATEGORY
//        // ---------------------------------------------------------
//
//        const administrative_count = await this.orm.searchCount(
//            "hr.employee",
//            [
//                ...domain,
//                ["category", "=", "administrative"],
//            ]
//        );
//
//        const service_count = await this.orm.searchCount(
//            "hr.employee",
//            [
//                ...domain,
//                ["category", "=", "service"],
//            ]
//        );
//
//        const judicial_count = await this.orm.searchCount(
//            "hr.employee",
//            [
//                ...domain,
//                ["category", "=", "judicial"],
//            ]
//        );
//
//        const military_count = await this.orm.searchCount(
//            "hr.employee",
//            [
//                ...domain,
//                ["category", "=", "military"],
//            ]
//        );
//
//
//        // ---------------------------------------------------------
//        // RELATED RECORDS
//        // ---------------------------------------------------------
//
//        const education_count = await this.orm.searchCount(
//            "employee.education",
//            []
//        );
//
//        const experience_count = await this.orm.searchCount(
//            "employee.experience",
//            []
//        );
//
//        const training_count = await this.orm.searchCount(
//            "employee.training",
//            []
//        );
//
//        const retirement_count = await this.orm.searchCount(
//            "employee.retirement",
//            []
//        );
//
//
//        // =========================================================
//        // UPDATE STATE
//        // =========================================================
//
//        this.state.total_count = total_count;
//        this.state.active_count = active_count;
//        this.state.inactive_count = inactive_count;
//
//        this.state.male_count = male_count;
//        this.state.female_count = female_count;
//        this.state.other_gender_count = other_gender_count;
//
//        this.state.current_count = current_count;
//        this.state.separated_count = separated_count;
//        this.state.detached_count = detached_count;
//        this.state.dismissed_count = dismissed_count;
//
//        this.state.retired_count = retired_count;
//        this.state.deceased_count = deceased_count;
//
//        this.state.administrative_count =
//            administrative_count;
//
//        this.state.service_count =
//            service_count;
//
//        this.state.judicial_count =
//            judicial_count;
//
//        this.state.military_count =
//            military_count;
//
//        this.state.education_count =
//            education_count;
//
//        this.state.experience_count =
//            experience_count;
//
//        this.state.training_count =
//            training_count;
//
//        this.state.retirement_count =
//            retirement_count;
//
//
//        // =========================================================
//        // RENDER CHARTS
//        // =========================================================
//
//        this.renderGenderChart();
//        this.renderStatusChart();
//        this.renderCategoryChart();
//    }
//
//
//    // =============================================================
//    // YEAR FILTER
//    // =============================================================
//
//    async onYearChange(ev) {
//
//        this.state.selected_year =
//            ev.target.value;
//
//        await this.loadData();
//
//        this.renderGenderChart();
//        this.renderStatusChart();
//        this.renderCategoryChart();
//    }
//
//
//    // =============================================================
//    // OPEN EMPLOYEE LIST
//    // =============================================================
//
//    async openEmployees(domain = []) {
//
//        await this.actionService.doAction({
//            type: "ir.actions.act_window",
//            name: "Employees",
//            res_model: "hr.employee",
//            views: [
//                [false, "list"],
//                [false, "form"],
//            ],
//            domain: domain,
//            target: "current",
//        });
//    }
//
//
//    openAllEmployees() {
//
//        return this.openEmployees(
//            this.getEmployeeDomain()
//        );
//    }
//
//
//    openActiveEmployees() {
//
//        return this.openEmployees([
//            ...this.getEmployeeDomain(),
//            ["active", "=", true],
//        ]);
//    }
//
//
//    openRetiredEmployees() {
//
//        return this.openEmployees([
//            ...this.getEmployeeDomain(),
//            ["job_status", "=", "متقاعد"],
//        ]);
//    }
//
//
//    openCurrentEmployees() {
//
//        return this.openEmployees([
//            ...this.getEmployeeDomain(),
//            ["job_status", "=", "برحال"],
//        ]);
//    }
//
//
//    // =============================================================
//    // GENDER CHART
//    // =============================================================
//
//    renderGenderChart() {
//
//        const canvas =
//            document.getElementById(
//                "employeeGenderChart"
//            );
//
//        if (!canvas) {
//            return;
//        }
//
//        if (this.genderChart) {
//            this.genderChart.destroy();
//        }
//
//        this.genderChart = new Chart(canvas, {
//
//            type: "doughnut",
//
//            data: {
//
//                labels: [
//                    "Male",
//                    "Female",
//                    "Other",
//                ],
//
//                datasets: [
//                    {
//                        data: [
//                            this.state.male_count,
//                            this.state.female_count,
//                            this.state.other_gender_count,
//                        ],
//
//                        backgroundColor: [
//                            "#4e73df",
//                            "#e83e8c",
//                            "#858796",
//                        ],
//
//                        borderWidth: 1,
//                    },
//                ],
//            },
//
//            options: {
//
//                responsive: true,
//
//                maintainAspectRatio: false,
//
//                plugins: {
//
//                    legend: {
//                        position: "bottom",
//                    },
//
//                    title: {
//                        display: true,
//                        text: "Employee Gender",
//                    },
//                },
//            },
//        });
//    }
//
//
//    // =============================================================
//    // JOB STATUS CHART
//    // =============================================================
//
//    renderStatusChart() {
//
//        const canvas =
//            document.getElementById(
//                "employeeStatusChart"
//            );
//
//        if (!canvas) {
//            return;
//        }
//
//        if (this.statusChart) {
//            this.statusChart.destroy();
//        }
//
//        this.statusChart = new Chart(canvas, {
//
//            type: "bar",
//
//            data: {
//
//                labels: [
//                    "Current",
//                    "Separated",
//                    "Detached",
//                    "Dismissed",
//                    "Retired",
//                    "Deceased",
//                ],
//
//                datasets: [
//                    {
//                        label: "Employees",
//
//                        data: [
//                            this.state.current_count,
//                            this.state.separated_count,
//                            this.state.detached_count,
//                            this.state.dismissed_count,
//                            this.state.retired_count,
//                            this.state.deceased_count,
//                        ],
//
//                        backgroundColor: [
//                            "#1cc88a",
//                            "#36b9cc",
//                            "#f6c23e",
//                            "#e74a3b",
//                            "#858796",
//                            "#5a5c69",
//                        ],
//
//                        borderRadius: 6,
//
//                        barThickness: 35,
//                    },
//                ],
//            },
//
//            options: {
//
//                responsive: true,
//
//                maintainAspectRatio: false,
//
//                plugins: {
//
//                    legend: {
//                        display: false,
//                    },
//
//                    title: {
//                        display: true,
//                        text: "Employee Job Status",
//                    },
//                },
//
//                scales: {
//
//                    y: {
//                        beginAtZero: true,
//
//                        ticks: {
//                            stepSize: 1,
//                        },
//                    },
//                },
//            },
//        });
//    }
//
//
//    // =============================================================
//    // CATEGORY CHART
//    // =============================================================
//
//    renderCategoryChart() {
//
//        const canvas =
//            document.getElementById(
//                "employeeCategoryChart"
//            );
//
//        if (!canvas) {
//            return;
//        }
//
//        if (this.categoryChart) {
//            this.categoryChart.destroy();
//        }
//
//        this.categoryChart = new Chart(canvas, {
//
//            type: "bar",
//
//            data: {
//
//                labels: [
//                    "Administrative",
//                    "Service",
//                    "Judicial",
//                    "Military",
//                ],
//
//                datasets: [
//                    {
//                        label: "Employees",
//
//                        data: [
//                            this.state.administrative_count,
//                            this.state.service_count,
//                            this.state.judicial_count,
//                            this.state.military_count,
//                        ],
//
//                        backgroundColor: [
//                            "#4e73df",
//                            "#36b9cc",
//                            "#1cc88a",
//                            "#f6c23e",
//                        ],
//
//                        borderRadius: 6,
//
//                        barThickness: 40,
//                    },
//                ],
//            },
//
//            options: {
//
//                responsive: true,
//
//                maintainAspectRatio: false,
//
//                plugins: {
//
//                    legend: {
//                        display: false,
//                    },
//
//                    title: {
//                        display: true,
//                        text: "Employee Categories",
//                    },
//                },
//
//                scales: {
//
//                    y: {
//                        beginAtZero: true,
//
//                        ticks: {
//                            stepSize: 1,
//                        },
//                    },
//                },
//            },
//        });
//    }
//}
//
//
//// =============================================================
//// TEMPLATE
//// =============================================================
//
//EmployeeDashboard.template =
//    "employee_dashboard.Main";
//
//
//// =============================================================
//// REGISTER CLIENT ACTION
//// =============================================================
//
//registry
//    .category("actions")
//    .add(
//        "employee_dashboard",
//        EmployeeDashboard
//    );


/** @odoo-module **/

import {
    Component,
    onWillStart,
    onMounted,
    onWillUnmount,
    useState,
} from "@odoo/owl";

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { loadJS } from "@web/core/assets";


class EmployeeDashboard extends Component {

    setup() {

        this.orm = useService("orm");
        this.actionService = useService("action");

        this.state = useState({

            // General
            total_count: 0,
            active_count: 0,
            inactive_count: 0,

            // Gender
            male_count: 0,
            female_count: 0,
            other_gender_count: 0,

            // Job status
            current_count: 0,
            separated_count: 0,
            detached_count: 0,
            dismissed_count: 0,
            retired_count: 0,
            deceased_count: 0,

            // Category
            administrative_count: 0,
            service_count: 0,
            judicial_count: 0,
            military_count: 0,

            // Related records
            education_count: 0,
            experience_count: 0,
            training_count: 0,
            retirement_count: 0,

            // Filter
            selected_year: "all",

            // Loading
            loading: true,
        });

        this.genderChart = null;
        this.statusChart = null;
        this.categoryChart = null;


        onWillStart(async () => {

            await loadJS(
                "https://cdn.jsdelivr.net/npm/chart.js"
            );

            await this.loadData();
        });


        onMounted(() => {

            this.renderCharts();
        });


        onWillUnmount(() => {

            this.destroyCharts();
        });
    }


    // =========================================================
    // DOMAIN
    // =========================================================

    getEmployeeDomain() {

        const domain = [];

        if (this.state.selected_year !== "all") {

            domain.push([
                "recruitment_date",
                ">=",
                `${this.state.selected_year}-01-01`,
            ]);

            domain.push([
                "recruitment_date",
                "<=",
                `${this.state.selected_year}-12-31`,
            ]);
        }

        return domain;
    }


    // =========================================================
    // LOAD DATA
    // =========================================================

    async loadData() {

        this.state.loading = true;

        const domain = this.getEmployeeDomain();


        // ---------------------------------------------------------
        // GENERAL
        // ---------------------------------------------------------

        const [
            total_count,
            active_count,
            inactive_count,

            male_count,
            female_count,
            other_gender_count,

            current_count,
            separated_count,
            detached_count,
            dismissed_count,
            retired_count,
            deceased_count,

            administrative_count,
            service_count,
            judicial_count,
            military_count,

            education_count,
            experience_count,
            training_count,
            retirement_count,
        ] = await Promise.all([

            this.orm.searchCount(
                "hr.employee",
                domain
            ),

            this.orm.searchCount(
                "hr.employee",
                [
                    ...domain,
                    ["active", "=", true],
                ]
            ),

            this.orm.searchCount(
                "hr.employee",
                [
                    ...domain,
                    ["active", "=", false],
                ]
            ),


            // Gender

            this.orm.searchCount(
                "hr.employee",
                [
                    ...domain,
                    ["emp_gender", "=", "male"],
                ]
            ),

            this.orm.searchCount(
                "hr.employee",
                [
                    ...domain,
                    ["emp_gender", "=", "female"],
                ]
            ),

            this.orm.searchCount(
                "hr.employee",
                [
                    ...domain,
                    ["emp_gender", "=", "other"],
                ]
            ),


            // Job Status

            this.orm.searchCount(
                "hr.employee",
                [
                    ...domain,
                    ["job_status", "=", "برحال"],
                ]
            ),

            this.orm.searchCount(
                "hr.employee",
                [
                    ...domain,
                    ["job_status", "=", "منفصل"],
                ]
            ),

            this.orm.searchCount(
                "hr.employee",
                [
                    ...domain,
                    ["job_status", "=", "منفک"],
                ]
            ),

            this.orm.searchCount(
                "hr.employee",
                [
                    ...domain,
                    ["job_status", "=", "معزول"],
                ]
            ),

            this.orm.searchCount(
                "hr.employee",
                [
                    ...domain,
                    ["job_status", "=", "متقاعد"],
                ]
            ),

            this.orm.searchCount(
                "hr.employee",
                [
                    ...domain,
                    ["job_status", "=", "وفات"],
                ]
            ),


            // Categories

            this.orm.searchCount(
                "hr.employee",
                [
                    ...domain,
                    ["category", "=", "administrative"],
                ]
            ),

            this.orm.searchCount(
                "hr.employee",
                [
                    ...domain,
                    ["category", "=", "service"],
                ]
            ),

            this.orm.searchCount(
                "hr.employee",
                [
                    ...domain,
                    ["category", "=", "judicial"],
                ]
            ),

            this.orm.searchCount(
                "hr.employee",
                [
                    ...domain,
                    ["category", "=", "military"],
                ]
            ),


            // Related records

            this.orm.searchCount(
                "employee.education",
                []
            ),

            this.orm.searchCount(
                "employee.experience",
                []
            ),

            this.orm.searchCount(
                "employee.training",
                []
            ),

            this.orm.searchCount(
                "employee.retirement",
                []
            ),
        ]);


        // =========================================================
        // UPDATE STATE
        // =========================================================

        Object.assign(this.state, {

            total_count,
            active_count,
            inactive_count,

            male_count,
            female_count,
            other_gender_count,

            current_count,
            separated_count,
            detached_count,
            dismissed_count,
            retired_count,
            deceased_count,

            administrative_count,
            service_count,
            judicial_count,
            military_count,

            education_count,
            experience_count,
            training_count,
            retirement_count,

            loading: false,
        });
    }


    // =========================================================
    // YEAR FILTER
    // =========================================================

    async onYearChange(ev) {

        this.state.selected_year =
            ev.target.value;

        await this.loadData();

        this.renderCharts();
    }


    // =========================================================
    // OPEN EMPLOYEES
    // =========================================================

    async openEmployees(domain = []) {

        await this.actionService.doAction({

            type: "ir.actions.act_window",

            name: "Employees",

            res_model: "hr.employee",

            views: [
                [false, "list"],
                [false, "form"],
            ],

            domain,

            target: "current",
        });
    }


    openAllEmployees() {

        return this.openEmployees(
            this.getEmployeeDomain()
        );
    }


    openActiveEmployees() {

        return this.openEmployees([
            ...this.getEmployeeDomain(),
            ["active", "=", true],
        ]);
    }


    openRetiredEmployees() {

        return this.openEmployees([
            ...this.getEmployeeDomain(),
            ["job_status", "=", "متقاعد"],
        ]);
    }


    openCurrentEmployees() {

        return this.openEmployees([
            ...this.getEmployeeDomain(),
            ["job_status", "=", "برحال"],
        ]);
    }


    // =========================================================
    // CHART MANAGEMENT
    // =========================================================

    destroyCharts() {

        if (this.genderChart) {
            this.genderChart.destroy();
            this.genderChart = null;
        }

        if (this.statusChart) {
            this.statusChart.destroy();
            this.statusChart = null;
        }

        if (this.categoryChart) {
            this.categoryChart.destroy();
            this.categoryChart = null;
        }
    }


    renderCharts() {

        this.renderGenderChart();
        this.renderStatusChart();
        this.renderCategoryChart();
    }


    // =========================================================
    // GENDER CHART
    // =========================================================

    renderGenderChart() {

        const canvas =
            document.getElementById(
                "employeeGenderChart"
            );

        if (!canvas) {
            return;
        }

        if (this.genderChart) {
            this.genderChart.destroy();
        }

        this.genderChart = new Chart(canvas, {

            type: "doughnut",

            data: {

                labels: [
                    "Male",
                    "Female",
                    "Other",
                ],

                datasets: [{
                    data: [
                        this.state.male_count,
                        this.state.female_count,
                        this.state.other_gender_count,
                    ],

                    backgroundColor: [
                        "#4e73df",
                        "#e83e8c",
                        "#858796",
                    ],

                    borderWidth: 2,
                    borderColor: "#ffffff",

                    hoverOffset: 6,
                }],
            },

            options: {

                responsive: true,

                maintainAspectRatio: false,

                cutout: "68%",

                plugins: {

                    legend: {
                        position: "bottom",

                        labels: {
                            usePointStyle: true,
                            padding: 18,
                            boxWidth: 8,
                        },
                    },

                    tooltip: {
                        padding: 10,
                    },
                },
            },
        });
    }


    // =========================================================
    // JOB STATUS CHART
    // =========================================================

    renderStatusChart() {

        const canvas =
            document.getElementById(
                "employeeStatusChart"
            );

        if (!canvas) {
            return;
        }

        if (this.statusChart) {
            this.statusChart.destroy();
        }

        this.statusChart = new Chart(canvas, {

            type: "bar",

            data: {

                labels: [
                    "Current",
                    "Separated",
                    "Detached",
                    "Dismissed",
                    "Retired",
                    "Deceased",
                ],

                datasets: [{
                    label: "Employees",

                    data: [
                        this.state.current_count,
                        this.state.separated_count,
                        this.state.detached_count,
                        this.state.dismissed_count,
                        this.state.retired_count,
                        this.state.deceased_count,
                    ],

                    backgroundColor: [
                        "#1cc88a",
                        "#36b9cc",
                        "#f6c23e",
                        "#e74a3b",
                        "#858796",
                        "#5a5c69",
                    ],

                    borderRadius: 7,

                    borderSkipped: false,

                    maxBarThickness: 42,
                }],
            },

            options: {

                responsive: true,

                maintainAspectRatio: false,

                plugins: {

                    legend: {
                        display: false,
                    },

                    tooltip: {
                        padding: 10,
                    },
                },

                scales: {

                    x: {
                        grid: {
                            display: false,
                        },

                        ticks: {
                            color: "#737980",
                        },
                    },

                    y: {

                        beginAtZero: true,

                        grid: {
                            color: "#eef0f2",
                        },

                        ticks: {
                            stepSize: 1,
                            color: "#8a9096",
                        },
                    },
                },
            },
        });
    }


    // =========================================================
    // CATEGORY CHART
    // =========================================================

    renderCategoryChart() {

        const canvas =
            document.getElementById(
                "employeeCategoryChart"
            );

        if (!canvas) {
            return;
        }

        if (this.categoryChart) {
            this.categoryChart.destroy();
        }

        this.categoryChart = new Chart(canvas, {

            type: "bar",

            data: {

                labels: [
                    "Administrative",
                    "Service",
                    "Judicial",
                    "Military",
                ],

                datasets: [{
                    label: "Employees",

                    data: [
                        this.state.administrative_count,
                        this.state.service_count,
                        this.state.judicial_count,
                        this.state.military_count,
                    ],

                    backgroundColor: [
                        "#4e73df",
                        "#36b9cc",
                        "#1cc88a",
                        "#f6c23e",
                    ],

                    borderRadius: 7,

                    borderSkipped: false,

                    maxBarThickness: 45,
                }],
            },

            options: {

                responsive: true,

                maintainAspectRatio: false,

                plugins: {

                    legend: {
                        display: false,
                    },

                    tooltip: {
                        padding: 10,
                    },
                },

                scales: {

                    x: {
                        grid: {
                            display: false,
                        },

                        ticks: {
                            color: "#737980",
                        },
                    },

                    y: {

                        beginAtZero: true,

                        grid: {
                            color: "#eef0f2",
                        },

                        ticks: {
                            stepSize: 1,
                            color: "#8a9096",
                        },
                    },
                },
            },
        });
    }
}


// =============================================================
// TEMPLATE
// =============================================================

EmployeeDashboard.template =
    "employee_dashboard.Main";


// =============================================================
// REGISTER CLIENT ACTION
// =============================================================

registry
    .category("actions")
    .add(
        "employee_dashboard",
        EmployeeDashboard
    );