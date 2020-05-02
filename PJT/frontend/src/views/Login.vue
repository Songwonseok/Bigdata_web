<template>
  <v-container id="user-profile" class="mt-12" fluid tag="section">
    <v-row justify="center">
      <v-col cols="12" md="8">
        <material-card color="orange lighten-2">
          <template v-slot:heading>
            <v-tabs v-model="tab" background-color="orange" fixed-tabs>
              <v-tab key="user">
                회원 로그인
              </v-tab>
              <v-tab key="admin">
                관리자 로그인
              </v-tab>
            </v-tabs>
          </template>
          <v-tabs-items v-model="tab">
            <v-tab-item key="user">
              <v-form>
                <v-container class="py-0">
                  <v-row>
                    <v-col cols="12" md="12">
                      <v-text-field
                        v-model="username"
                        :error-messages="usernameErrors"
                        label="아이디"
                        required
                        prepend-icon="mdi-account"
                        type="text"
                        @input="$v.username.$touch()"
                        @blur="$v.username.$touch()"
                      />
                    </v-col>

                    <v-col cols="12" md="12">
                      <v-text-field
                        v-model="password"
                        :error-messages="passwordErrors"
                        prepend-icon="mdi-lock"
                        type="password"
                        label="비밀번호"
                        required
                        @input="$v.password.$touch()"
                        @blur="$v.password.$touch()"
                      />
                    </v-col>
                    <v-col cols="12" class="text-right">
                      <v-btn color="orange lighten-2" @click="submit"
                        >Login</v-btn
                      >
                    </v-col>
                  </v-row>
                </v-container>
              </v-form>
            </v-tab-item>
            <v-tab-item key="admin">
              <v-form>
                <v-container class="py-0">
                  <v-row>
                    <v-col cols="12" md="12">
                      <v-text-field
                        v-model="username"
                        :error-messages="usernameErrors"
                        label="아이디"
                        required
                        prepend-icon="mdi-account"
                        type="text"
                        @input="$v.username.$touch()"
                        @blur="$v.username.$touch()"
                      />
                    </v-col>

                    <v-col cols="12" md="12">
                      <v-text-field
                        v-model="password"
                        :error-messages="passwordErrors"
                        prepend-icon="mdi-lock"
                        type="password"
                        label="비밀번호"
                        required
                        @input="$v.password.$touch()"
                        @blur="$v.password.$touch()"
                      />
                    </v-col>
                    <v-col cols="12" class="text-right">
                      <v-btn color="orange lighten-2" @click="adminSubmit"
                        >Login</v-btn
                      >
                    </v-col>
                  </v-row>
                </v-container>
              </v-form>
            </v-tab-item>
          </v-tabs-items>
        </material-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { validationMixin } from "vuelidate";
import { required, email, minLength } from "vuelidate/lib/validators";
import { mapActions } from "vuex";
import MaterialCard from "@/components/MaterialCard";
export default {
  components: {
    MaterialCard,
  },
  mixins: [validationMixin],
  validations: {
    username: { required },
    email: { required, email },
    password: { required, minLength: minLength(6) },
  },
  data: () => ({
    username: "",
    email: "",
    password: "",
    tab: null,
  }),
  computed: {
    usernameErrors() {
      const errors = [];
      if (!this.$v.username.$dirty) return errors;
      !this.$v.username.required && errors.push("아이디를 입력해주세요.");
      return errors;
    },
    passwordErrors() {
      const errors = [];
      if (!this.$v.password.$dirty) return errors;
      !this.$v.password.minLength &&
        errors.push("비밀번호는 6글자 이상이어야 합니다.");
      !this.$v.password.required && errors.push("비밀번호를 입력해주세요.");
      return errors;
    },
  },
  methods: {
    ...mapActions("data", ["login", "adminLogin"]),
    submit() {
      this.$v.$touch();
      const params = {
        username: this.username,
        password: this.password,
      };

      this.login(params);
    },
    adminSubmit() {
      this.$v.$touch();
      const params = {
        username: this.username,
        password: this.password,
      };
      this.adminLogin(params);
    },
  },
};
</script>
