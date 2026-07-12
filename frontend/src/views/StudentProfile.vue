<template>
    <div v-if="role == 'student'">
    <nav class="navbar bg-body-tertiary">
      <div class="container-fluid">
          <router-link to="/student" class="text-decoration-none text-dark fs-3 fw-bold">Student Dashboard</router-link>
      </div>
    </nav> 
    <router-link to="/student" class="btn btn-outline-secondary m-3">← Back</router-link>
    <div class="card m-3 border border-dark">
        <div class="card-header">Student Details</div>
        <div class="card-body">
            <span class="fw-bold m-2" v-if="editMode">Note: <br>1. Name cannot be edited<br>2. Educational details can be edited only if there are no applications applied by you.</span><br>
            <table class="table mx-1">
                <tr>
                    <th width="220">Full Name</th>
                    <td v-if="!editMode">{{ student.full_name }}</td>
                    <td v-else>
                        <input class="form-control" v-model="student.full_name" type="text" disabled>
                    </td>
                </tr>
                <tr>
                    <th>CGPA</th>
                    <td v-if="!editMode">{{ student.cgpa }}</td>
                    <td v-else-if="student.application == 0">
                        <input class="form-control" v-model="student.cgpa" type="number" min="0" max="10" step="0.1">
                    </td>
                    <td v-else>
                        <input class="form-control" v-model="student.cgpa" type="number" min="0" max="10" step="0.1" disabled>
                    </td>
                </tr>
                <tr>
                    <th>Branch</th>
                    <td v-if="!editMode">{{ student.branch  }}</td>
                    <td v-else-if="student.application == 0">
                        <input class="form-control" v-model="student.branch" type="text">
                    </td>
                    <td v-else>
                        <input class="form-control" v-model="student.branch" type="text" disabled>
                    </td>
                </tr>
                <tr>
                    <th>Education</th>
                    <td v-if="!editMode" >{{ student.education }}</td>
                    <td v-else-if="student.application == 0">
                        <input class="form-control" v-model="student.education" type="text" >
                    </td>
                    <td v-else>
                        <input class="form-control" v-model="student.education" type="text" disabled>
                    </td>
                </tr>
                <tr>
                    <th>Skills</th>
                    <td v-if="!editMode">{{ student.skills }}</td>
                    <td v-else>
                        <input class="form-control" v-model="student.skills" type="text">
                    </td>
                </tr>
                <tr>
                    <th>Experience</th>
                    <td v-if="!editMode">{{ student.experience }}</td>
                    <td v-else>
                        <input class="form-control" v-model="student.experience" type="text">
                    </td>
                </tr>
                <tr>
                    <th>Resume</th>
                    <td v-if="!editMode">
                        <button v-if="this.student.resume_path != null" @click="downloadResume" class="btn btn-primary bg-primary btn-sm my-2">Download Resume</button>
                        <span v-else class="fw-bold">Not uploaded</span>
                    </td>
                    <td v-else>
                        <button class="btn btn-primary bg-primary m-2 text-white" v-if="!updateResume && !resume" @click="allowUpdateResume">Update New Resume</button>
                        <div v-else-if="updateResume">
                            <span class="fw-bold">Note: Updating resume would discard old resume if any</span>
                            <input type="file" class="form-control m-2" @change="selectResume" accept="application/pdf, .pdf">
                            <button class="btn btn-success" @click="saveUpdatedResume">Save Resume</button>
                            <button class="btn btn-danger" @click="notupdateResume">Cancel</button>
                        </div>
                        <div v-else>
                            <span class="fw-bold">Resume provided successfully</span>
                        </div>
                    </td>
                </tr>
                <tr>
                    <th>Contact</th>
                    <td v-if="!editMode">{{ student.contact }}</td>
                    <td v-else>
                        <input class="form-control" v-model="student.contact" type="tel">
                    </td>
                </tr>
                <tr>
                    <th>LinkedIn Url</th>
                    <td v-if="!editMode">
                        <a v-if="student.linkedin_url" :href="student.linkedin_url" target="_blank">{{ student.linkedin_url }}</a>
                        <span v-else class="fw-bold">Not Provided</span>
                    </td>
                    <td v-else>
                        <input type="url" v-model="student.linkedin_url" class="form-control m-1"> 
                    </td>
                </tr>
                <tr>
                    <th>GitHub Url</th>
                    <td v-if="!editMode">
                        <a  v-if="student.github_url" :href="student.github_url" target="_blank">{{ student.github_url }}</a>
                        <span v-else class="fw-bold">Not Provided</span>
                    </td>
                    <td v-else>
                        <input type="url" v-model="student.github_url" class="form-control m-1"> 
                    </td>
                </tr>
                
            </table>
            <div class="mt-3 d-flex gap-2">
                <button v-if="!editMode" class="btn btn-warning" @click="editAccessOn()">Edit</button>
                <button v-else class="btn btn-danger" @click="editAccessOff">Cancel</button>
                <button v-if="editMode" class="btn btn-success" @click="editProfile()">Save</button>
            </div>
        </div>
    </div>
    
    </div>
    <div v-else>
    <div class="card m-4 bg-warning" style="max-width: 370px;">
      <span class="card-header">You are not a Student. Please <router-link to="/login">login</router-link></span>
    </div>
  </div>
</template>
<script>
import axios from 'axios';

export default {
    data(){
        const role = localStorage.getItem("role");
        return {
            "role": role,
            "student" : {},
            "editMode" : false ,
            "resume" : '',
            "updateResume" : false
        }
    },

    methods : {
        async loadProfile(){
            try {
                const response = await axios.get("http://127.0.0.1:5000/student/profile",{
                    headers: { Authorization: `Bearer ${localStorage.getItem("token")}` }
                });
                this.student = response.data ;
                // console.log(this.student);
                

            } catch (e) {
                alert(e.response?.data?.message || "Something went wrong")
            }
        },
        editAccessOn(){
            this.editMode = true
        },
        async editAccessOff(){
            this.editMode = false
            this.resume = ''
            await this.loadProfile()
        },
        isUrlSyntaxValid(string) {
            return URL.canParse(string);
        },
        async editProfile(){
            try {
                let conf = confirm("Are you sure you want to save?")
                if(conf){
                    if(this.student.github_url){
                        if(this.student.github_url.length != 0){
                            if(!this.isUrlSyntaxValid(this.student.github_url)){
                                alert("Invalid GitHub URL format");
                                return ;
                            }
                    }
                    }

                    if(this.student.linkedin_url){
                        if(this.student.linkedin_url.length != 0){
                            if(!this.isUrlSyntaxValid(this.student.linkedin_url)){
                                alert("Invalid LinkedIn URL format");
                                return ;
                            }
                    }
                    }
                    if(this.updateResume){
                        if(!this.saveUpdatedResume()){
                            return ;
                        }
                    }

                    const contactRegex=/^[6-9]\d{9}$/
                    if(!contactRegex.test(this.student.contact)){
                        alert("Please enter a valid 10-digit contact number")
                        return
                    }

                    if(this.student.skills.trim().length < 1){
                        alert("Skills cannot be empty")
                        return ;
                    }

                    const formData = new FormData()
                    formData.append("cgpa" , this.student.cgpa )
                    formData.append("branch" , this.student.branch) 
                    formData.append( "education" , this.student.education) 
                    formData.append("skills" , this.student.skills)
                    formData.append("experience" , this.student.experience)
                    formData.append("resume" , this.resume)
                    formData.append("contact" , this.student.contact),
                    formData.append("github_url" , this.student.github_url)
                    formData.append("linkedin_url" , this.student.linkedin_url)

                    const response = await axios.put("http://127.0.0.1:5000/student/profile/update",formData,{
                        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` }
                    });
                    alert(response.data.message) ;
                    this.editMode = false 
                    await this.loadProfile()
                    this.resume = ''
                }
            } catch (error) {
                console.log(error);
                
                alert(error.response?.data?.message || "Something went wrong")

            }
        },
        allowUpdateResume(){
            this.updateResume = true 
        },
        notupdateResume(){
            this.resume = ""
            this.updateResume = false 
        },
        saveUpdatedResume(){
            // console.log(this.resume);
            
            if(!this.resume){
                alert("No resume provided");
                return false;
            }
            this.updateResume = false 
            return true;
        },
        selectResume(event){
            this.resume = event.target.files[0]
            console.log(this.resume);
            
        },
        async downloadResume(){
            try{
                const response = await axios.get("http://127.0.0.1:5000/student/resume",{responseType: "blob",headers:{Authorization:`Bearer ${localStorage.getItem("token")}`}})

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
    },
    async mounted(){
        if(this.role == 'student'){
            await this.loadProfile()
        }
    }
    
}

</script>