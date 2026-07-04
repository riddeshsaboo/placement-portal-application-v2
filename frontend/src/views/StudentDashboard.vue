<template>
  <div>
    <nav class="navbar bg-body-tertiary">
      <div class="container-fluid">
          <h3 class="fw-bold">Student Dashboard</h3>
          <div>
            <router-link to="/student/profile" class="btn btn-outline-secondary d-inline-flex align-items-center m-2 rounded-pill transition-all">
              <img src="../../public/user-profile.png" class="rounded-circle border border-2 border-white" alt="Profile Avatar"  style="width: 28px; height: 28px; object-fit: cover;">
              <span class="fw-semibold text-dark small">{{dashboard.student.full_name}}</span>
            </router-link>
            <button class="btn btn-danger m-1" @click="logOut">Logout </button>
          </div>
      </div>
    </nav> 

    <div class="card mt-3" v-if="jobs.length > 0">
      <div class="card-header">Available Job Postings</div>
      <div class="card-body">
        <input class="form-control mb-3" placeholder="Search using company name or job title or skills required" v-model="search_job">
        <table class="table table-hover" v-if="filteredJobs.length > 0">
          <thead>
            <tr>
              <th>Sr</th>
              <th>Company</th>
              <th>Title</th>
              <th>Package(LPA)</th>
              <th>Minimum CGPA</th>
              <th>Skills Required</th>
              <th>Deadline</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(job, index) in filteredJobs" :key="job.id">
              <td>{{ index + 1 }}</td>
              <td>{{ job.company_name }}</td>
              <td>{{ job.title }}</td>
              <td>{{ job.salary || "Not Disclosed" }}</td>
              <td>{{ job.min_cgpa || "Not Required" }}</td>
              <td>{{ job.skills_required || "Not Disclosed" }}</td>
              <td>{{ formatDate(job.deadline) }}</td>
              <td><router-link :to="`/student/job_posting/${job.id}`" class="btn btn-primary btn-sm">View</router-link></td>
            </tr>
          </tbody>
        </table>
        <div v-else>
          No job postings found try searching something different
        </div>
      </div>
    </div>
    <div v-else class="card mt-3">
      <span class="fw-bold m-2">No job postings available</span>
    </div>
    

    <div class="card mt-4" v-if="applications.length > 0">
      <div class="card-header">My Applications</div>
      <div class="card-body">
        <table class="table table-hover">
          <thead>
            <tr>
              <th>Sr</th>
              <th>Company</th>
              <th>Job Title</th>
              <th>Applied On</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(application, index) in applications" :key="application.id">
              <td>{{ index + 1 }}</td>
              <td>{{ application.company_name }}</td>
              <td>{{ application.title }}</td>
              <td>{{ formatDate(application.applied_at) }}</td>
              <td>
                <span class="badge bg-warning text-dark" v-if="application.status === 'applied'">Applied</span>
                <span class="badge bg-primary" v-else-if="application.status === 'shortlisted'">Shortlisted</span>
                <span class="badge bg-primary-subtle" v-else-if="application.status === 'interview_scheduled'">Interview Scheduled</span>
                <span class="badge bg-success" v-else-if="application.status === 'selected'">Selected</span>
                <span class="badge bg-success" v-else-if="application.status === 'placed'">Placed</span>
                <span class="badge bg-danger" v-else>Rejected</span>
              </td>
              <td>
                <router-link :to="`/student/application/${application.id}`" class="btn btn-success mx-2" >View Application</router-link> 
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <div v-else class="card mt-3">
      <span class="fw-bold m-2">You have not applied to any job postings yet</span>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      jobs: [],
      search_job: "",
      applications: [],
      dashboard : {
        student: {}
      }
    };
  },
  async mounted() {
    await this.loadDashboard()
    await this.loadJobs();
    await this.loadApplications();
  },
  methods: {
    logOut() {
      localStorage.removeItem("token");
      localStorage.removeItem("role");
      this.$router.push("/login");
    },
    async loadDashboard(){
      try{
        const response = await axios.get("http://127.0.0.1:5000/student/dashboard",{
          headers: { Authorization: `Bearer ${localStorage.getItem("token")}` }
        })
        this.dashboard = response.data ;
        console.log(this.dashboard);
        
      }catch(e){
        console.log(e.response);
        console.log(e.response?.status);
        console.log(e.response?.data);
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
    async loadJobs() {
      try {
        const response = await axios.get("http://127.0.0.1:5000/student/job_postings", {
          headers: { Authorization: `Bearer ${localStorage.getItem("token")}` }
        });
        this.jobs = response.data;
      } catch (e) {
        console.log(e);
        console.log(e.response);
        console.log(e.response?.data);
        alert(e.response.data.message || "Something went wrong");
      }
    },
    formatDate(date) {
      return new Date(date).toLocaleString("en-GB");
    },
    async loadApplications() {
      try {
        const response = await axios.get("http://127.0.0.1:5000/student/applications", {
          headers: { Authorization: `Bearer ${localStorage.getItem("token")}` }
        });
        this.applications = response.data;
        
      } catch (e) {
        console.log(e);
        console.log(e.response);
        console.log(e.response?.data);
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

    async accept_offer(application_id){
        try{
            let conf = confirm("Accepting this offer would close all other applications. Are you sure?")
            console.log(application_id)
            if(conf){
                const response = await axios.put(`http://127.0.0.1:5000/student/application/${application_id}/accept`,{},{headers: { Authorization: `Bearer ${localStorage.getItem("token")}` }})
                this.loadApplications()
                alert(response.data.message);
                // console.log(response.data.message);
                
            }
        }catch(e){
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

    async reject_offer(application_id){
        try{
            console.log(application_id)
            let conf = confirm("Reject this offer? Are you sure?")
            if(conf){
                const response = await axios.put(`http://127.0.0.1:5000/student/application/${application_id}/reject`,{},{headers: { Authorization: `Bearer ${localStorage.getItem("token")}` }})
                this.loadApplications()
                console.log(response.data.message);
                // alert(response.data.message);
            }
        }catch(e){
          if(e.response?.status == 401){
              alert("Session expired. Please login again.");
              localStorage.removeItem("token");
              localStorage.removeItem("role");
              this.$router.push("/");
              return;
          }
          alert(e.response?.data?.message || e.response?.data?.msg || "Something went wrong");
        }
    }
  },
  computed: {
    filteredJobs() {
    const query = this.search_job.toLowerCase().trim();

    return this.jobs.filter(job => {
        const skills = job.skills_required
            ? job.skills_required.toLowerCase().split(",").map(skill => skill.trim())
            : [];

        return (
            job.company_name.toLowerCase().includes(query) ||
            job.title.toLowerCase().includes(query) ||
            skills.some(skill => skill.includes(query))
        );
    });
  }
  }
};
</script>