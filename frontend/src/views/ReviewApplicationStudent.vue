<template>
<div class="container mt-4">
    <h2>Review Application</h2>
    <div class="card mt-3">
        <div class="card-header">
            Company Details
        </div>
        <div class="card-body">
            <table class="table">
                <tr>
                    <th width="220">Company Name</th>
                    <td>{{ application.company.company_name }}</td>
                </tr>
                <tr>
                    <th>Industry</th>
                    <td>{{ application.company.industry }}</td>
                </tr>
                <tr>
                    <th>Company Location</th>
                    <td>{{ application.company.location }}</td>
                </tr>
                <tr>
                    <th>Company Website</th>
                    <td><a :href="application.company.website" target="_blank">{{ application.company.website }}</a></td>
                </tr>
                <tr>
                    <th>Company Description</th>
                    <td>{{ application.company.description }}</td>
                </tr>
                <!-- <tr>
                    <th>Resume</th>
                    <td>
                        <a :href="application.student.resume" target="_blank">View Resume</a>
                    </td>
                </tr> -->
            </table>
        </div>
    </div>
    <div class="card mt-3">
        <div class="card-header">
            Application Details
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
                        <span v-if="application.status == 'selected'" class="badge bg-success">Selected</span>
                        <span v-if="application.status == 'placed'" class="badge bg-success">Placed</span>
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
                        <button class="btn btn-info bg-info my-2 btn-sm" @click="downloadOfferLetter(application.id)">View Offer Letter</button>
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
                <tr v-if="application.status == 'selected'">
                    <th>Actions</th>
                    <td>
                        <button class="btn btn-primary bg-primary m-2 text-white" v-if="application.status == 'selected'" @click="accept_offer(application.id)">Accept</button>
                        <button class="btn btn-danger bg-danger m-2 text-white" v-if="application.status == 'selected'" @click="reject_offer(application.id)">Reject</button>
                    </td>
                </tr>
            </table>
        </div>
    </div>

    <div class="card mt-3">
        <div class="card-header">
            Application Progress
        </div>

        <div class="card-body d-flex justify-content-between align-items-center" v-if="application.status != 'rejected'">

            <div class="text-center">
                <div class="rounded-circle border border-dark d-flex justify-content-center align-items-center bg-success text-white" v-if="application_stage > -1" style="width:60px;height:60px;">1</div>
                <!-- <div class="rounded-circle border border-dark d-flex justify-content-center align-items-center bg-warning" v-if="application_stage == 0" style="width:60px;height:60px;">1</div> -->
                <small>Applied</small>
            </div>

            <div class="flex-grow-1 border-top mx-2"></div>

            <div class="text-center">
                <div class="rounded-circle border border-dark d-flex justify-content-center align-items-center bg-success text-white" v-if="application_stage >= 1" style="width:60px;height:60px;">2</div>
                <div class="rounded-circle border border-dark d-flex justify-content-center align-items-center bg-warning" v-if="application_stage < 1" style="width:60px;height:60px;">2</div>
                <small>Shortlisted</small>
            </div>

            <div class="flex-grow-1 border-top mx-2"></div>

            <div class="text-center">
                <div class="rounded-circle border border-dark d-flex justify-content-center align-items-center bg-success text-white" v-if="application_stage >= 2" style="width:60px;height:60px;">3</div>
                <div class="rounded-circle border border-dark d-flex justify-content-center align-items-center bg-warning" v-if="application_stage < 2" style="width:60px;height:60px;">3</div>
                <small>Interview Scheduled</small>
            </div>

            <div class="flex-grow-1 border-top mx-2"></div>

            <div class="text-center">
                <div class="rounded-circle border border-dark d-flex justify-content-center align-items-center bg-success text-white" v-if="application_stage >= 3" style="width:60px;height:60px;">4</div>
                <div class="rounded-circle border border-dark d-flex justify-content-center align-items-center bg-warning" v-if="application_stage < 3" style="width:60px;height:60px;">4</div>
                <small>Selected</small>
            </div>

            <div class="flex-grow-1 border-top mx-2"></div>

            <div class="text-center">
                <div class="rounded-circle border border-dark d-flex justify-content-center align-items-center bg-success text-white" v-if="application_stage >= 4" style="width:60px;height:60px;">5</div>
                <div class="rounded-circle border border-dark d-flex justify-content-center align-items-center bg-warning" v-if="application_stage < 4" style="width:60px;height:60px;">5</div>
                <small>Placed</small>
            </div>

        </div>
        <div v-else class="card-body">
            <span class="fw-bold bg-danger text-white p-2">Application Rejected</span>
            <p class="my-2">Sorry your application was rejected by the company</p>
        </div>
    </div>
    <div class="card mt-3" v-if="application.status == 'shortlisted'">
        <div class="card-header" >
            Points to be noted for Shortlisted candidates
        </div>
        <div class="card-body">
            1. It is advised to be active to recieve interview details if you qualify for the interview round. <br>
            2. Once rejected you cannot re-apply to the placement drive. <br>
            3. Company has the right to reject the application without any prior notification. <br>
        </div>
    </div>
    <div class="card mt-3" v-if="application.status == 'interview_scheduled'">
        <div class="card-header" >
            Points to be noted for Interview
        </div>
        <div class="card-body">
            1. It is advised to join the interview using the link provided atleast 10 minutes before the scheduled date and time. <br> 
            2. Interviews cannot be rescheduled and failing to be present may lead to rejection of application. <br>
            3. Once rejected you cannot re-apply to the placement drive. <br>
            4. Company has the right to reject the application without any prior notification. <br> 
            5. Be present in professional attire and all the required original documents and proofs with you. <br>
            6. If the interview is offline, company would provide the Google Maps link of the venue, you have to be present there atleast 1 hour before the scheduled time. <br>
        </div>
    </div>
    <div class="card mt-3" v-if="application.status == 'selected'">
        <div class="card-header" >
            Points to be noted for placement
        </div>
        <div class="card-body">
            1. Accepting an offer would lead to rejection of all other ongoing applications. <br>
            2. As vacancies may be limited, accepting offer is based on First Come First Basis - if vacancies are filled before you accept an offer your application will be auto-rejected. <br>
            3. You must be present at the given joining date on time. <br>
            4. Company holds the right to terminate you at any time without any reason. <br>
            5. Rejecting an offer would NOT affect any other ongoing application.  <br>
            6. Please read the offer letter carefully before accepting or rejecting any placement offer. <br>
            7. By accepting an offer you agree to all the terms and conditions mentioned in the Offer letter. <br>
        </div>
    </div>
</div>
</template>

<script>
import axios from "axios"

export default{
    data(){
        return{
            application:{
                student:{},
                job:{},
                company:{}
            },
            application_stage: 0
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
            const response = await axios.get(`http://127.0.0.1:5000/student/application/${this.$route.params.id}`, { headers:{ Authorization:`Bearer ${localStorage.getItem("token")}` } })
            this.application=response.data

            if(this.application.status == 'shortlisted'){
                this.application_stage = 1 
            }else if(this.application.status == 'interview_scheduled'){
                this.application_stage = 2
            }else if(this.application.status == 'selected'){
                this.application_stage = 3
            }else if(this.application.status == 'placed'){
                this.application_stage = 4
            }else if(this.application.status == 'rejected'){
                this.application_stage = -1
            }else{ //applied
                this.application_stage = 0
            }
        },
        formatDate(date){
            return new Date(date).toLocaleString("en-GB")
        },
        async accept_offer(application_id){
            try{
                let conf = confirm("Accepting this offer would close all other applications. Are you sure?")
                console.log(application_id)
                if(conf){
                    const response = await axios.put(`http://127.0.0.1:5000/student/application/${application_id}/accept`,{},{headers: { Authorization: `Bearer ${localStorage.getItem("token")}` }})
                    this.loadApplication()
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
                    this.loadApplication()
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
                this.loadApplication()
            }
        },

        async downloadOfferLetter(id){
            try{
                const response = await axios.get(`http://127.0.0.1:5000/student/application/${id}/offer_letter`,{responseType:"blob",headers:{Authorization:`Bearer ${localStorage.getItem("token")}`}})

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
        }
       
        


        


    }
}
</script>