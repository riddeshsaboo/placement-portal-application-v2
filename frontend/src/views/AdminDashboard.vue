<template>
    <div v-if="role == 'admin' " class="m-2">
        <nav class="navbar bg-body-tertiary">
            <div class="container-fluid">
                <h3 class="fw-bold">Admin Dashboard</h3>
                <div>
                    <button v-if="!showchart" class="btn btn-warning m-2" @click="()=>{showchart = !showchart}">Show Chart</button>
                    <button v-else class="btn btn-warning m-2" @click="()=>{showchart = !showchart}">Hide Chart</button>
                    <button class="btn btn-success" @click="monthlyReport">Export Monthly Report</button>
                    <button class="btn btn-primary ms-2" @click="sendReminders">Send Interview Reminders</button>
                    <button class="btn btn-danger m-1" @click="logout">Logout </button>
                </div>
            </div>

        </nav>
        <div class="row g-3 mb-4">
            <div class="col-md-3">
                <div class="card border-success h-100">
                    <div class="card-body text-center">
                        <h5 class="text-success">Total Companies</h5>
                        <h2 class="fw-bold">{{ total_companies }}</h2>
                        <hr>
                        <h5 class="text-success">Active Companies</h5>
                        <h2 class="fw-bold">{{ active_companies }}</h2>
                    </div>
                </div>
            </div>

            <div class="col-md-3">
                <div class="card border-primary h-100">
                    <div class="card-body text-center">
                        <h5 class="text-primary">Total Students</h5>
                        <h2 class="fw-bold">{{ total_students }}</h2>
                        <hr>
                        <h5 class="text-primary">Active Students</h5>
                        <h2 class="fw-bold">{{ active_students }}</h2>
                    </div>
                </div>
            </div>

            <div class="col-md-3">
                <div class="card border-warning h-100">
                    <div class="card-body text-center">
                        <h5 class="text-warning">Total Job Postings</h5>
                        <h2 class="fw-bold">{{ total_job_postings }}</h2>
                        <hr>
                        <h5 class="text-warning">Active Job Postings</h5>
                        <h2 class="fw-bold">{{ active_job_postings }}</h2>
                    </div>
                </div>
            </div>

            <div class="col-md-3">
                <div class="card border-info h-100">
                    <div class="card-body text-center">
                        <h5 class="text-info">Applications</h5>
                        <h2 class="fw-bold">{{ total_applications }}</h2>
                        <hr>
                        <h5 class="text-info">Applicants Placed</h5>
                        <h2 class="fw-bold">{{ applicants_placed }}</h2>
                    </div>
                </div>
            </div>

        </div>

        <div v-if="showchart" class="container mt-5">
            <div class="card shadow">
                <div class="card-body">
                    <Bar :data="dashboardData" :options="chartOptions"/>
                </div>
            </div>
        </div>

        <div id="companies" v-if="companies.length > 0" class="mt-3">
            <h2>Companies</h2>
            <div class="input-group m-2">
                <input type="search" v-model="search_company" placeholder="Search companies by name / industry" class="form-control" style="max-width: 370px"  />
            </div>
            <div class="table-responsive m-2" style="max-height:400px; overflow-y:auto;">
                <table class="table table-hover">
                    <thead class="table-success">
                        <tr>
                            <th>ID</th>
                            <th>Company</th>
                            <th>Industry</th>
                            <th>Status</th>
                            <th width="220">Actions</th>
                        </tr>
                    </thead>

                    <tbody>
                    <tr v-for="company in filteredCompanies" :key="company.id">
                        <td>{{ company.id }}</td>
                        <td>{{ company.company_name }}</td>
                        <td>{{ company.industry }}</td>
                        <td>
                            <span v-if="company.approval_status == 'pending'" class="badge bg-warning">Pending</span>
                            <span v-if="company.approval_status == 'approved'" class="badge bg-success">Approved</span>
                            <span v-if="company.approval_status == 'blacklisted'" class="badge bg-dark">Blacklisted</span>
                            <span v-if="company.approval_status == 'rejected'" class="badge bg-danger">Rejected</span>
                        </td>
                        <td>
                            <div class="d-flex gap-2">
                                <router-link :to = "`/admin/company/${company.id}`" class="btn btn-info btn-sm">View Profile</router-link>
                                <button v-if="company.approval_status == 'pending'" @click="update_company_status(company.id,'approved')" class="btn btn-success btn-sm ">Approve</button>
                                <button v-if="company.approval_status == 'pending'" @click="update_company_status(company.id,'rejected')" class="btn btn-danger btn-sm ">Reject</button>
                                <button v-if="company.approval_status == 'approved'" @click="update_company_status(company.id,'blacklisted')" class="btn btn-danger btn-sm">Blacklist</button>
                                <button v-if="company.approval_status == 'rejected'" @click="update_company_status(company.id,'approved')" class="btn btn-success btn-sm">Approve</button>
                                <button v-if="company.approval_status == 'blacklisted'" @click="update_company_status(company.id,'approved')" class="btn btn-success btn-sm">Unblacklist</button>
                            </div>
                        </td>
                    </tr>
                    </tbody>
                </table>
            </div>
        </div>
        <div v-else>
            <h2>No companies registered yet</h2>
        </div>

        <div id="students" v-if="students.length > 0">
            <h2>Students</h2>
            <div class="input-group m-2">
                <input type="search" v-model="search_student" placeholder="Search students by name / id / contact" class="form-control" style="max-width: 370px"  />
            </div>
            <div class="table-responsive m-2" style="max-height:400px; overflow-y:auto;">
                <table class="table table-hover">
                    <thead class="table-primary">
                        <tr>
                            <th>ID</th>
                            <th>Name</th>
                            <th>Branch</th>
                            <th>Contact</th>
                            <th>is_active</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="student in filteredStudents" :key="student.id">
                            <td>{{ student.id }}</td>
                            <td>{{ student.full_name }}</td>
                            <td>{{ student.branch }}</td>
                            <td>{{ student.contact || "NA" }}</td>
                            <td>
                                <span v-if="student.is_active == true" class="badge bg-success">Yes</span>
                                <span v-else class="badge bg-danger">No</span>
                            </td>
                            <td>
                                <div class="d-flex gap-2">
                                    <router-link :to = "`/admin/student/${student.id}`" class="btn btn-info btn-sm">View Profile</router-link>
                                    <button v-if="student.is_active == true" @click="update_student_status(student.id,0)" class="btn btn-danger btn-sm ">Deactivate</button>
                                    <button v-else @click="update_student_status(student.id,1)" class="btn btn-success btn-sm ">Activate</button>
                                </div>
                            </td>
                        </tr>
                    </tbody>
            </table>
            </div>
        </div>
        <div v-else>
            <h2>No students registered yet</h2>
        </div>

        <div v-if="job_postings.length > 0" id="job_postings">
            <br><br>
            <h2>Job Postings</h2>
            <div class="input-group m-2">
                <input type="search" v-model="search_job" placeholder="Search Job postings by title / company name / status" class="form-control" style="max-width: 370px"  />
            </div>
            <div class="table-responsive m-2" style="max-height:400px; overflow-y:auto;">
                <table class="table table-hover">
                    <thead class="table-warning">
                        <tr>
                            <th>ID</th>
                            <th>Title</th>
                            <th>Company</th>
                            <th>Salary</th>
                            <th>Min CGPA</th>
                            <th>Skills required</th>
                            <th>Vacancies</th>
                            <th>Created at</th>
                            <th>Deadline</th>
                            <th>Status</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="posting in filteredJobs" :key="posting.id">
                            <td>{{ posting.id }}</td>
                            <td>{{ posting.title }}</td>
                            <td>{{ posting.company_name }}</td>
                            <td>{{ posting.salary || "Not Disclosed" }}</td>
                            <td>{{ posting.min_cgpa || "Not Disclosed"}}</td>
                            <td>{{ posting.skills_required || "Not Disclosed" }}</td>
                            <td>{{ posting.vacancies }}</td>
                            <td>{{ formatDate(posting.created_at) }}</td>
                            <td>{{ formatDate(posting.deadline) }}</td>
                            <td>
                                <span v-if="posting.status == 'pending'" class="badge bg-warning">Pending</span>
                                <span v-if="posting.status == 'approved'" class="badge bg-success">Approved</span>
                                <span v-if="posting.status == 'closed'" class="badge bg-danger">Closed</span>
                                <span v-if="posting.status == 'rejected'" class="badge bg-danger">Rejected</span>
                            </td>
                            <td>
                                <div class="d-flex gap-2">
                                <button v-if="posting.status == 'pending'" @click="updatePostingStatus(posting.id,'approved')" class="btn btn-success btn-sm " >Approve</button>
                                <button v-if="posting.status == 'pending'" @click="updatePostingStatus(posting.id,'rejected')" class="btn btn-danger btn-sm "> Reject</button>
                                <button v-if="posting.status == 'approved'" @click="updatePostingStatus(posting.id,'closed')" class="btn btn-danger btn-sm "> Close</button>
                                <span v-if="posting.status == 'closed'">NA</span>
                                <span v-if="posting.status == 'rejected'">NA</span>
                                </div>
                            </td>
                        </tr>
                    </tbody>
            </table>
            </div>
        </div>
        <div v-else>
            <br><br>
            <h2>No Job postings yet</h2>
        </div>

        <div v-if="applications.length > 0" id="applications">
            <h2>Applications</h2>
            <div class="input-group m-2">
                <input type="search" v-model="search_application" placeholder="Search Applications by student name / company name / status" class="form-control" style="max-width: 370px"  />
            </div>
            <div class="table-responsive m-2" style="max-height:400px; overflow-y:auto;">
                <table class="table table-hover">
                    <thead class="table-info">
                        <tr>
                            <th>ID</th>
                            <th>Student Name</th>
                            <th>Company Name</th>
                            <th>Job title</th>
                            <th>Status</th>
                            <th>Applied on</th>
                            <th>Joining Date</th>
                            <th>Offer Letter</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="appl in filteredApplications" :key="appl.id">
                            <td>{{ appl.id }}</td>
                            <td>{{ appl.student_name }}</td>
                            <td>{{ appl.company_name }}</td>
                            <td>{{ appl.job_title }}</td>
                            <td>
                                <span class="badge bg-warning text-dark" v-if="appl.status === 'applied'">Applied</span>
                                <span class="badge bg-primary" v-else-if="appl.status === 'shortlisted'">Shortlisted</span>
                                <span class="badge bg-primary-subtle" v-else-if="appl.status === 'interview_scheduled'">Interview Scheduled</span>
                                <span class="badge bg-success" v-else-if="appl.status === 'selected'">Selected</span>
                                <span class="badge bg-success" v-else-if="appl.status === 'placed'">Placed</span>
                                <span class="badge bg-danger" v-else>Rejected</span>
                            </td>
                            <td>{{ formatDate(appl.applied_at) }}</td>
                            <td v-if="appl.joining_date">{{ formatDate(appl.joining_date) }}</td>
                            <td v-else>NA</td>
                            <td v-if="appl.offer_letter">
                                <button @click="download_offer_letter(appl.id)" class="btn btn-info">View offer letter</button>
                            </td>
                            <td v-else>NA</td>
                        </tr>
                    </tbody>
            </table>
            </div>
        </div>
        <div v-else>
            <h2>No Applications yet</h2>
        </div>

    </div>
    <div v-else>
        <h1>You are not admin! Please <router-link to="/login">Login</router-link></h1>
    </div>
</template>

<script>
import axios from 'axios';
import {Chart as ChartJS,CategoryScale,LinearScale,BarElement,Title,Tooltip,Legend} from "chart.js";

import { Bar } from "vue-chartjs";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

export default {
    data(){
        const role = localStorage.getItem("role");
        return {
            role : role ,
            total_students : 0, 
            active_students : 0,
            total_companies : 0,
            active_companies : 0,
            total_job_postings : 0,
            active_job_postings : 0,
            total_applications : 0,
            applicants_placed : 0,
            companies: [],
            search_company: "",
            students: [],
            search_student: "",
            job_postings: [], 
            search_job: "",
            applications: [],
            search_application: "",
            showchart: false 
        }
    },

    async mounted() {
        if (this.role !== "admin") {
            if(this.role == "student"){
                this.$router.push("/student")
            }
            else if(this.role == "company"){
                this.$router.push("/company")
            }
            else{
                this.$router.push("/login")
            }
        }
        else{
            await this.loadData()
            await this.loadCompanies() 
            await this.loadStudents()
            await this.loadJobPostings(),
            await this.loadApplications()
        }

    },

    methods : {
        logout() {
            localStorage.removeItem("token");
            localStorage.removeItem("role");
            this.$router.push("/login");
        },

        async loadData(){
            const response = await axios.get("http://127.0.0.1:5000/admin/dashboard", {headers: {Authorization: `Bearer ${localStorage.getItem("token")}`}})

            this.total_students = response.data.total_students
            this.active_students = response.data.active_students
            this.total_companies = response.data.total_companies
            this.active_companies = response.data.active_companies
            this.total_job_postings = response.data.total_job_postings
            this.active_job_postings = response.data.active_job_postings
            this.total_applications = response.data.total_applications
            this.applicants_placed = response.data.applicants_placed
        },

        async loadCompanies(){
            const companiesResponse = await axios.get("http://127.0.0.1:5000/admin/companies", {headers: {Authorization:`Bearer ${localStorage.getItem("token")}`}})
            
            this.companies = companiesResponse.data
            // console.log(this.companies)
        },

        async update_company_status(company_id,status){
            // console.log("Approved", company_id);
            await axios.put(`http://127.0.0.1:5000/admin/company/${company_id}/status`,{status : status},{headers: {Authorization:`Bearer ${localStorage.getItem("token")}`}})

            await this.loadData()
            await this.loadCompanies()
        },

        async loadStudents(){
            const studentsResponse = await axios.get("http://127.0.0.1:5000/admin/students", {headers: {Authorization:`Bearer ${localStorage.getItem("token")}`}})
            
            this.students = studentsResponse.data
        },

        async update_student_status(student_id,status){
            await axios.put(`http://127.0.0.1:5000/admin/student/${student_id}/status`,{status : status},{headers: {Authorization:`Bearer ${localStorage.getItem("token")}`}})

            await this.loadData()
            await this.loadStudents()     
        },

        async loadJobPostings(){
            const response = await axios.get("http://127.0.0.1:5000/admin/job_postings",{headers:{Authorization:`Bearer ${localStorage.getItem("token")}`}})
            this.job_postings = response.data
        },

        async updatePostingStatus(posting_id,status){
            await axios.put(`http://127.0.0.1:5000/admin/job_posting/${posting_id}/status`,{status: status},{headers:{Authorization:`Bearer ${localStorage.getItem("token")}`}})
            await this.loadJobPostings()
            await this.loadData()
        },

        formatDate(dateString){
            return new Date(dateString).toLocaleString("en-GB")
        },

        async loadApplications(){
            try {
                const response = await axios.get("http://127.0.0.1:5000/admin/applications", {headers: {Authorization:`Bearer ${localStorage.getItem("token")}`}})
                this.applications = response.data
            } catch (e) {
                if(e.response?.status == 401){
                    alert("Session expired. Please login again.");
                    localStorage.removeItem("token");
                    localStorage.removeItem("role");
                    this.$router.push("/");
                    return;
                }
                alert(e.response?.data?.message || e.response?.data?.msg || "Something went wrong");
            }
            // console.log(this.applications);
        },

        async download_offer_letter(application_id){
            try{
                const response = await axios.get(`http://127.0.0.1:5000/admin/application/${application_id}/offer_letter`,{responseType: "blob",headers:{Authorization:`Bearer ${localStorage.getItem("token")}`}})

                const url = window.URL.createObjectURL(response.data)
                window.open(url,"_blank")
            }catch(e){
                if(e.response?.status == 401){
                    alert("Session expired. Please login again.");
                    localStorage.removeItem("token");
                    localStorage.removeItem("role");
                    this.$router.push("/");
                    return;
                }
                // console.log(e.response);
                alert(e.response?.data?.message || e.response?.data?.msg || "Something went wrong");
            }
        },

        async monthlyReport(){
            try{
                const response = await axios.post("http://127.0.0.1:5000/admin/monthly_report",{},{headers:{Authorization:`Bearer ${localStorage.getItem("token")}`}})
                alert(response.data.message || "Success");
                
            }catch(e){
                if(e.response?.status == 401){
                    alert("Session expired. Please login again.");
                    localStorage.removeItem("token");
                    localStorage.removeItem("role");
                    this.$router.push("/");
                    return;
                }
                // console.log(e.response);
                alert(e.response?.data?.message || e.response?.data?.msg || "Something went wrong");
            }
        },

        async sendReminders(){
            try{
                const response = await axios.post("http://127.0.0.1:5000/admin/reminders",{},{headers:{Authorization:`Bearer ${localStorage.getItem("token")}`}})
                alert(response.data.message || "Success");

            }catch(e){
                if(e.response?.status == 401){
                    alert("Session expired. Please login again.");
                    localStorage.removeItem("token");
                    localStorage.removeItem("role");
                    this.$router.push("/");
                    return;
                }
                // console.log(e.response);
                alert(e.response?.data?.message || e.response?.data?.msg || "Something went wrong");
            }
        },
    },

    computed: {
    filteredCompanies(){
        return this.companies.filter(company =>
            company.company_name.toLowerCase().includes(
                this.search_company.toLowerCase()
            )
            ||
            company.industry.toLowerCase().includes(
                this.search_company.toLowerCase()
            )
        )
    },

    filteredStudents(){
        return this.students.filter(student =>
            student.id.toString().includes(this.search_student)
            ||
            student.full_name.toLowerCase().includes(
                this.search_student.toLowerCase()
            )
            ||
            (student.contact || "").toLowerCase().includes(this.search_student.toLowerCase())
            )
    },

    filteredJobs(){
        return this.job_postings.filter(job =>
            job.title.toString().toLowerCase().includes(this.search_job.toLowerCase())
            ||
            job.company_name.toLowerCase().includes(this.search_job.toLowerCase())
            ||
            job.status.toLowerCase().includes(this.search_job.toLowerCase())
            )
    },

    filteredApplications(){
        return this.applications.filter(appl =>
            appl.student_name.toLowerCase().includes(this.search_application.toLowerCase())
            ||
            appl.company_name.toLowerCase().includes(this.search_application.toLowerCase())
            ||
            appl.status.toLowerCase().includes(this.search_application.toLowerCase())
            )
    },
    dashboardData(){
        return{
            labels:["Total Students", "Active Students", "Total Companies", "Active Companies", "Total Job Postings", "Active Job Postings","Applications", "Placed Students"],

            datasets:[{
                    label:"Count",
                    data:[this.total_students, this.active_students, this.total_companies, this.active_companies, this.total_job_postings, this.active_job_postings,this.total_applications, this.applicants_placed ],
                    backgroundColor:["blue", "skyblue", "green", "lightgreen", "orange", "gold", "lightseagreen", "cyan"],
            }]
        }
    },

    chartOptions(){
        return{
            responsive:true,
            indexAxis:"y",
            plugins:{
                legend:{display:false},
                title:{display:true,text: "Placement Portal Overview"}
            },
            scales:{
                x:{beginAtZero:true}
            }
        }
    },
    
    },
    components: {
        Bar
    },

}
</script>