<template>
<div class="container mt-4">
    <router-link to="/company" class="btn btn-outline-secondary mb-3">← Back</router-link>
    <h2>Manage Job Posting</h2>
    <div class="card mt-3 border border-dark">
        <div class="card-header">Job Details</div>
        <div class="card-body">
            <table class="table">
                <tr>
                    <th width="220">Title</th>
                    <td v-if="!editMode">{{ this.job.title }}</td>
                    <td v-else>
                        <input class="form-control" v-model="job.title" type="text">
                    </td>
                </tr>
                <tr>
                    <th>Description</th>
                    <td v-if="!editMode">{{ this.job.description || "NA" }}</td>
                    <td v-else>
                        <textarea class="form-control" v-model="job.description" rows = "4"></textarea>
                    </td>
                </tr>
                <tr>
                    <th>Salary</th>
                    <td v-if="!editMode">{{ this.job.salary || "Not Disclosed" }}</td>
                    <td v-else>
                        <input class="form-control" v-model="job.salary" type="number" step="0.1">
                    </td>
                </tr>
                <tr>
                    <th>Minimum CGPA</th>
                    <td v-if="!editMode" >{{ this.job.min_cgpa || "Not Disclosed" }}</td>
                    <td v-else>
                        <input class="form-control" v-model="job.min_cgpa" type="number" min="0" max="10" step="0.1" >
                    </td>
                </tr>
                <tr>
                    <th>Skills Required</th>
                    <td v-if="!editMode">{{ this.job.skills_required || "Not Disclosed" }}</td>
                    <td v-else>
                        <input class="form-control" v-model="job.skills_required" type="text">
                    </td>
                </tr>
                <tr>
                    <th>Location</th>
                    <td v-if="!editMode">{{ this.job.job_location || "Not Disclosed" }}</td>
                    <td v-else>
                        <input class="form-control" v-model="job.job_location" type="text">
                    </td>
                </tr>
                <tr>
                    <th>Vacancies</th>
                    <td v-if="!editMode" >{{ this.job.vacancies }}</td>
                    <td v-else>
                        <input class="form-control" v-model="job.vacancies" type="number" :min="1">
                    </td>
                </tr>
                <tr>
                    <th>Created At</th>
                    <td >{{ formatDate(this.job.created_at) }}</td>
                    
                </tr>
                <tr>
                    <th>Deadline</th>
                    <td v-if="!editMode">{{ formatDate(this.job.deadline) }}</td>
                    <td v-else>
                        <input class="form-control" v-model="job.deadline" type="datetime-local">
                    </td>
                </tr>
                <tr>
                    <th>Status</th>
                    <td>
                        <span class="badge bg-success text-white" v-if="job.status == 'approved'">Approved</span>
                        <span class="badge bg-warning text-dark" v-else-if="job.status == 'pending'">Pending</span>
                        <span class="badge bg-secondary text-white" v-else-if="job.status == 'closed'">Closed</span>
                        <span class="badge bg-danger text-white" v-else>Rejected</span>
                    </td>
                </tr>
            </table>
            <div class="mt-3 d-flex gap-2">
                <button v-if="!editMode & (this.job.status == 'pending' || this.job.status == 'approved')" class="btn btn-warning" @click="editAccessOn()">Edit</button>

                <button v-if="editMode" class="btn btn-success" @click="editJobPosting()"> Save</button>

                <button v-if="editMode" class="btn btn-secondary" @click="editAccessOff()"> Cancel</button>

                <button v-if = "this.job.status != 'closed' && this.job.status != 'rejected' " class="btn btn-danger" @click="updatePostingStatus(this.$route.params.id, 'closed')"> Close Job Posting</button>

            </div>
        </div>
    </div>
    <div id="applications" v-if="this.applications.length > 0" class="card mt-3 mb-3 border border-dark p-3">
    <h2>Applications</h2>
        <input class="form-control mb-3" placeholder="Search applicants by name/ status" v-model="search_application">
        <div class="table-responsive m-2" style="max-height:500px; overflow-y:auto;">
            <table class="table table-hover">
            <thead class="table-primary">
                <tr>
                    <th>Sr</th>
                    <th>Name</th>
                    <th>Branch</th>
                    <th>CGPA</th>
                    <th>Applied On</th>
                    <th>Status</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(application,index) in filteredApplications" :key="application.id">
                    <td>{{ index+1 }}</td>
                    <td>{{ application.student_name }}</td>
                    <td>{{ application.branch }}</td>
                    <td>{{ application.cgpa }}</td>
                    <td>{{ formatDate(application.applied_at) }}</td>
                    <td>
                        <span v-if="application.status == 'applied'" class="badge bg-warning">Applied</span>
                        <span v-if="application.status == 'shortlisted'" class="badge bg-primary text-white">Shortlisted</span>
                        <span v-if="application.status == 'interview_scheduled'" class="badge bg-primary-subtle text-white">Interview Scheduled</span>
                        <span v-if="application.status == 'selected'" class="badge bg-success">Selected</span>
                        <span v-if="application.status == 'placed'" class="badge bg-success">Placed</span>
                        <span v-if="application.status == 'rejected'" class="badge bg-danger">Rejected</span>
                    </td>
                    <td>
                        <router-link class="btn btn-primary btn-sm" :to="`/company/application/${application.id}`">Review</router-link>
                    </td>
                </tr>
            </tbody>
            </table>
        </div>
    </div>
    <div v-else>
        <h2>No applicants</h2>
    </div>
</div>
</template>

<script>
import axios from "axios"
export default {
    data() { 
        return { 
            job: {} ,
            editMode:false,
            applications:[],
            search_application:"",
    
        } 
    },
    async mounted() { 
        await this.loadJob() 
        await this.loadApplications()
    },
    methods: {
        async loadJob() {
            try{
                const response = await axios.get(`http://127.0.0.1:5000/company/job_posting/${this.$route.params.id}`, { headers: { Authorization: `Bearer ${localStorage.getItem("token")}` } })
                this.job = response.data;
                this.job.deadline = new Date(this.job.deadline).toISOString().slice(0,16)
            }
            catch(e){
                if(e.response?.status == 401){
                    alert("Session expired. Please login again.");
                    localStorage.removeItem("token");
                    localStorage.removeItem("role");
                    this.$router.push("/");
                    return;
                }
                alert(e.response?.data?.message || e.response?.data?.msg || "Something went wrong");
                this.$router.push("/company")
            }
        },
        formatDate(date){
            if(!date) {
                return "NA";
            }
            return new Date(date.replace(" GMT","")).toLocaleString("en-GB")
        },
        async loadApplications() {
            try{
                const response = await axios.get(`http://127.0.0.1:5000/company/job_posting/${this.$route.params.id}/applications`, { headers: { Authorization: `Bearer ${localStorage.getItem("token")}` } })
                this.applications = response.data
            }
            catch(e){
                if(e.response?.status == 401){
                    alert("Session expired. Please login again.");
                    localStorage.removeItem("token");
                    localStorage.removeItem("role");
                    this.$router.push("/");
                    return;
                }
                alert(e.response?.data?.message || e.response?.data?.msg || "Something went wrong");
            }
        },

        editAccessOn(){
            if (this.job.status == "approved" && this.applications.length > 0){
                alert("You cannot edit a job posting which has 1 or more applications");
                return ;
            }
            else{
                this.editMode = true ;
            }
        },

        async editAccessOff(){
            this.editMode = false ;
            await this.loadJob();
        },

        async editJobPosting(){
            if (this.job.status == "approved" && this.applications.length > 0){
                alert("You cannot edit a job posting which has 1 or more applications");
                return ;
            }
            else{
                try {
                    await axios.put(`http://127.0.0.1:5000/company/job_posting/${this.$route.params.id}`,{
                        "title" : this.job.title,
                        "description" : this.job.description, 
                        "salary" : this.job.salary,
                        "skills_required" : this.job.skills_required,
                        "min_cgpa" : this.job.min_cgpa, 
                        "job_location" : this.job.job_location, 
                        "deadline" : this.job.deadline, 
                        "vacancies" : this.job.vacancies,
                    },{headers: {Authorization:`Bearer ${localStorage.getItem("token")}`}})

                    this.editMode = false
                    await this.loadJob()
                    alert("Job updated successfully")
                } catch (error) {
                    alert(error.response.data.message)
                }
            }
        },

        async updatePostingStatus(posting_id,status){
            let conf = confirm("Are you sure you want to close this Job?");

            if(conf && status == "closed"){
                await axios.put(`http://127.0.0.1:5000/company/job_posting/${posting_id}/status`,{status: status},{headers:{Authorization:`Bearer ${localStorage.getItem("token")}`}})
                editMode = false
                await this.loadJob()
                await this.loadApplications()

            }
        },
    },
    computed:{
        filteredApplications(){
            return this.applications.filter(application =>
                application.student_name.toLowerCase().includes(
                    this.search_application.toLowerCase()
                )
                ||
                application.status.toLowerCase().includes(
                    this.search_application.toLowerCase()
                )
            )
        }
    }
}
</script>