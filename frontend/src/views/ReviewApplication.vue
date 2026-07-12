<template>
<div class="container mt-4">
    <router-link to="/company" class="btn btn-outline-secondary mb-3">← Back</router-link>
    <h2>Review Application</h2>
    <div class="card mt-3 border border-dark">
        <div class="card-header">
            Student Details
        </div>
        <div class="card-body">
            <table class="table">
                <tr>
                    <th width="220">Name</th>
                    <td>{{ application.student.name }}</td>
                </tr>
                <tr>
                    <th>Email</th>
                    <td>{{ application.student.email }}</td>
                </tr>
                <tr>
                    <th>Contact</th>
                    <td>{{ application.student.contact }}</td>
                </tr>
                <tr>
                    <th>Branch</th>
                    <td>{{ application.student.branch }}</td>
                </tr>
                <tr>
                    <th>CGPA</th>
                    <td>{{ application.student.cgpa }}</td>
                </tr>
                <tr>
                    <th>GitHub URL</th>
                    <td>
                        <a v-if="application.student.github_url" :href="`${application.student.github_url}`" target="_blank" class="btn btn-link">{{ application.student.github_url }}</a> 
                        <span v-else>Not Provided</span>
                    </td>
                </tr>
                <tr>
                    <th>LinkedIn URL</th>
                    <td>
                        <a v-if="application.student.linkedin_url" :href="`${application.student.linkedin_url}`" target="_blank" class="btn btn-link">{{ application.student.linkedin_url }}</a> 
                        <span v-else>Not Provided</span>
                    </td>
                </tr>
                <tr>
                    <th>Resume</th>
                    <td>
                       <button class="btn btn-primary btn-sm bg-primary my-2 text-white" @click="downloadResume(application.student.id)">View Resume</button>
                       <button v-if="!ats" class="btn btn-info btn-sm bg-info m-2 text-white" @click="checkResume(application.id)">Check Resume Match Score</button>
                    </td>
                </tr>
                <tr v-if="ats">
                    <th>ATS</th>
                    <td>
                    <span class="m-1"><span class="fw-bold">Resume Score</span> : {{ resume_score }}</span><br>
                    <span class="m-1"><span class="fw-bold">Matched Skills</span> :{{matched_skills || " None"}}</span><br>
                    <span class="m-1"><span class="fw-bold">Missing Skills</span> : {{ missing_skills || "None" }}</span><br>
                    <span v-if="recommendation == 'Excellent Match'" class="badge bg-success m-1">Recommendation: {{ recommendation }}</span>
                    <span v-else-if="recommendation == 'Good Match'" class="badge bg-warning m-1">Recommendation: {{ recommendation }}</span>
                    <span v-else class="badge bg-danger m-1">{{ recommendation }}</span>
                        
                    </td>
                </tr>
            </table>
        </div>
    </div>
    <div class="card mt-3 border border-dark">
        <div class="card-header">
            Application
        </div>
        <div class="card-body">
            <table class="table">
                <tr>
                    <th width="220">Job</th>
                    <td>{{ application.job.title }}</td>
                </tr>
                <tr>
                    <th>Status</th>
                    <td>
                        <span v-if="application.status == 'applied'" class="badge bg-warning">Applied</span>
                        <span v-if="application.status == 'shortlisted'" class="badge bg-primary text-white">Shortlisted</span>
                        <span v-if="application.status == 'interview_scheduled'" class="badge bg-primary-subtle">Interview Scheduled</span>
                        <span v-if="application.status == 'selected'" class="badge bg-success text-white">Selected</span>
                        <span v-if="application.status == 'placed'" class="badge bg-success text-white">Placed</span>
                        <span v-if="application.status == 'rejected'" class="badge bg-danger text-white">Rejected</span>
                    </td>
                </tr>
                <tr>
                    <th>Last Feedback</th>
                    <td><pre style="white-space: pre-wrap;">{{ application.feedback || "Not provided"}}</pre></td>
                </tr>
                <tr v-if="application.status == 'selected' || application.status == 'placed'">
                    <th>Offer Letter</th>
                    <td>
                        <button class="btn btn-info bg-info btn-sm my-2 text-white" @click="downloadOfferLetter(application.id)">View Offer Letter</button>
                    </td>
                </tr>
                <tr v-if="application.status == 'selected' || application.status == 'placed'">
                    <th>Joining Date</th>
                    <td>{{ formatDate(application.joining_date )}}</td>
                </tr>
                <tr>
                    <th>Applied At</th>
                    <td>{{ formatDate(application.applied_at) }}</td>
                </tr>
                <tr v-if="application.status =='interview_scheduled'">
                    <th>Interview Meeting link</th>
                    <td><a :href="application.meeting_link" target="_blank">{{ application.meeting_link }}</a></td>
                </tr>
                <tr v-if="application.status =='interview_scheduled'">
                    <th>Meeting Date and Time</th>
                    <td>{{ formatDate(application.interview_datetime) }}</td>
                </tr>
            </table>
        </div>
    </div>
    <div class="card mt-3 mb-3 border border-dark">
        <div class="card-header">
            Actions
        </div>
        <div class="card-body">
            <div v-if="flag" class="mb-3">
                <label class="form-label">Interview Date and Time</label>
                <input type="datetime-local" class="form control mb-3 mx-2" v-model="interview_datetime" :min="now">
                <br>
                <label class="form-label">Meeting link</label>
                <input type="url" class="form-control" v-model="meeting_link">
            </div>
            <div class="mb-3" v-if="application.status != 'selected' && application.status != 'rejected' && application.status != 'placed'">
                <label class="form-label">Feedback</label>
                <input type="textbox" class="form-control" v-model="feedback">
            </div>
            <div v-if="application.status == 'interview_scheduled'" class="mb-3">
                <label class="form-label">Joining Date</label>
                <input type="datetime-local" class="form-control mb-3" v-model="joining_date" :min="now">
                <label class="form-label">Offer Letter (PDF)</label>
                <input type="file" class="form-control" accept=".pdf" @change="selectOfferLetter" >
            </div>
            <button v-if="application.status=='applied'" class="btn btn-success" @click="shortlist">Shortlist</button>
            <button v-if="application.status=='shortlisted'" class="btn btn-success" @click="interview">Schedule Interview</button>
            <button v-if="application.status=='interview_scheduled'" class="btn btn-success" @click="select">Select</button>
            <button v-if="application.status != 'placed' && application.status != 'selected' && application.status != 'rejected'" class="btn btn-danger ms-2" @click="reject">Reject</button>
            <span v-if="application.status == 'selected'" class="fw-bold">The offer is not accepted yet by the candidate, status will update if the candidate accepts/rejects the offer</span>
            <span v-if="application.status == 'rejected'" class="fw-bold">NA</span>
            <span v-if="application.status == 'placed'" class="fw-bold">Offer accepted by the candidate</span>
        </div>
    </div>
</div>
</template>

<script>
import axios from "axios"

export default{
    data(){
        return{
            "application":{
                "student":{},
                "job":{}
            },
            "flag": false,
            "feedback": "",
            "interview_datetime": "",
            "meeting_link": "",
            "now" : "",
            "offer_letter":null,
            "joining_date": "",
            "ats" : false,
            "resume_score": 0,
            "recommendation":'',
            "matched_skills":'',
            "missing_skills":''
        }
    },
    async mounted(){
        await this.loadApplication()
        const now = new Date()
        const year = now.getFullYear()
        const month = String(now.getMonth() + 1).padStart(2, "0")
        const day = String(now.getDate()).padStart(2, "0")
        const hours = String(now.getHours()).padStart(2, "0")
        const minutes = String(now.getMinutes()).padStart(2, "0")
        this.now = `${year}-${month}-${day}T${hours}:${minutes}`
    },
    methods:{
        async loadApplication(){
            const response = await axios.get(`http://127.0.0.1:5000/company/application/${this.$route.params.id}`, { headers:{ Authorization:`Bearer ${localStorage.getItem("token")}` } })
            this.application=response.data

            if(this.application.status == 'shortlisted'){  
                // ensuring interview = true if next stage will be interview scheduled, so user can put data like link and datetime of interview
                this.flag = true 
            }
            else{
                this.flag = false 
            }
        },
        formatDate(date){
            if(!date) {
                return "NA";
            }
            return new Date(date.replace(" GMT","")).toLocaleString("en-GB")
        },

        async shortlist(){
            try{
                let conf = confirm("Are you sure you want to Shortlist this candidate?")
                if(conf && this.application.status == 'applied'){
                    await axios.put(`http://127.0.0.1:5000/company/application/${this.$route.params.id}/shortlist`,{
                        "feedback" : this.feedback
                    },{ headers:{ Authorization:`Bearer ${localStorage.getItem("token")}` } })
                    await this.loadApplication()
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
        async reject(){
            try{
                let conf = confirm("Are you sure you want to Reject this candidate?")
                if(conf){
                    await axios.put(`http://127.0.0.1:5000/company/application/${this.$route.params.id}/reject`, {
                        "feedback" : this.feedback
                    },{ headers:{ Authorization:`Bearer ${localStorage.getItem("token")}` } })
                    await this.loadApplication()
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

        isUrlSyntaxValid(string) {
            return URL.canParse(string);
        },

        async interview(){
            try{
                let conf = confirm("Are you sure you want to Interview this candidate?")
                if(conf && this.application.status == 'shortlisted'){
                    if(!this.interview_datetime || !this.meeting_link){
                        alert("Required fields missing")
                        return ; 
                    }
                    if(!this.interview_datetime.trim().length === 0 || this.meeting_link.trim().length === 0){
                        alert("Required fields missing")
                        return ;
                    }
                    if(!this.isUrlSyntaxValid(this.meeting_link)){
                        alert("Invalid meeting link format")
                        return ;
                    }
                    await axios.put(`http://127.0.0.1:5000/company/application/${this.$route.params.id}/interview_scheduled`,{
                        "interview_datetime" : this.interview_datetime ,
                        "meeting_link" : this.meeting_link,
                        "feedback" : this.feedback
                    } ,{ headers:{ Authorization:`Bearer ${localStorage.getItem("token")}` } })
                    await this.loadApplication()
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

        async select(){
            try{
                let conf = confirm("Are you sure you want to Select this candidate?")
                if(!this.offer_letter){
                    alert("Please upload the offer letter");
                    return ;
                }
                if(!this.joining_date){
                    alert("Please provide the joining date");
                    return ;
                }
                if(conf && this.application.status == 'interview_scheduled'){
                    const formData = new FormData()
                    formData.append("offer_letter", this.offer_letter)
                    formData.append("feedback", this.feedback)
                    formData.append("joining_date", this.joining_date)
                    await axios.put(`http://127.0.0.1:5000/company/application/${this.$route.params.id}/select`,formData ,{ headers:{ Authorization:`Bearer ${localStorage.getItem("token")}` } })
                    await this.loadApplication()
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

        selectOfferLetter(event){
            this.offer_letter = event.target.files[0]
        },

        async downloadResume(student_id){
            try{
                const response = await axios.get(`http://127.0.0.1:5000/company/student/${student_id}/resume`,{responseType:"blob",headers:{Authorization:`Bearer ${localStorage.getItem("token")}`}})

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
                alert(e.response?.data?.message || e.response?.data?.msg || "Something went wrong");
            }
        },

        async downloadOfferLetter(application_id){
            try{
                const response = await axios.get(`http://127.0.0.1:5000/company/application/${application_id}/offer_letter`,{responseType:"blob",headers:{Authorization:`Bearer ${localStorage.getItem("token")}`}})

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
                alert(e.response?.data?.message || e.response?.data?.msg || "Something went wrong");
            }
        },

        async checkResume(id){
            try {
                const response = await axios.post(`http://127.0.0.1:5000/company/resume_screener/${id}`,{},{headers:{Authorization:`Bearer ${localStorage.getItem("token")}`}})
                
                this.resume_score = response.data.resume_score
                this.recommendation = response.data.recommendation
                this.matched_skills = response.data.matched_skills.join(", ")
                this.missing_skills = response.data.missing_skills.join(", ")
                this.ats = true 
                
            } catch (e) {
                console.log(e);
            }
        }



    }
}
</script>