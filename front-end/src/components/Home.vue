<template>
    <div>
        <p>主页</p>
        <!--
        <p>随机数：{{ randomNumber }}</p>
        <a-button @click="getRandom" type="primary">生成</a-button>
        -->
        <div>
            <p>文件：<a-input-number id="file_id" v-model="file_id" />
                <a-button @click="getFile" type='primary'>获取</a-button>
            </p>
        </div>
        <a-list item-layout="vertical" :data-source="text_flows" :pagination="pagination">
            <a-list-item slot="renderItem" slot-scope="item">
                <div style="display: block">
                    <a-card hoverable style="max-width: 80%;
                    margin:auto;
                    border-radius: 7px;
                    background-color: rgba(250, 250, 250, 0.9)" :bodyStyle="card_body_style">
                        {{ item.src_text }}
                    </a-card>
                </div>
                <div style="display: block; max-width: 80%; margin:auto;">
                    <a-textarea :auto-size="{ minRows: 3 }" :value="file_id" @change="update(item.id)" />
                </div>
            </a-list-item>
        </a-list>
    </div>
</template>

<script>
import axios from 'axios'

var text_flows = []
export default {
    data () {
        return {
            randomNumber: 0,
            file_id: 0,
            text_flows,
            pagination: {
                pageSize: 20
            },
            card_body_style: {
                textAlign: 'left'
            }
        }
    },
    methods: {
        getRandom() {
            const path = 'http://localhost:5000/api/random'
            axios.get(path)
            .then(response => {
                this.randomNumber = response.data.randomNumber
            })
            .catch(error => {
                console.log(error)
            })
        },
        getFile() {
            const path = 'http://localhost:5000/api/file/get/' + this.file_id
            axios.get(path).then(response => {
                console.log(response)
                this.text_flows = response.data.text_flows
            })
        },
        created () {
            this.getRandom()
        },
        update(id) {
            //const path = 'http://localhost:5000/api/'
            console.log(id)
        }
    }
}
</script>