<template>
  <v-container id="user-profile" class="mt-12" fluid tag="section">
    <v-row justify="center">
      <v-col cols="12" md="8">
        <material-card color="green">
          <template v-slot:heading>
            <div class="display-5 font-weight-light">
              회원 가입
            </div>
          </template>

          <v-form>
            <v-container class="py-0">
              <v-row>
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="username"
                    :error-messages="usernameErrors"
                    label="아이디"
                    class="purple-input"
                    required
                    @input="$v.username.$touch()"
                    @blur="$v.username.$touch()"
                  />
                </v-col>

                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="email"
                    :error-messages="emailErrors"
                    label="E-mail"
                    class="purple-input"
                    required
                    @input="$v.email.$touch()"
                    @blur="$v.email.$touch()"
                  />
                </v-col>

                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="password"
                    :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
                    :error-messages="passwordErrors"
                    :type="show1 ? 'text' : 'password'"
                    label="비밀번호"
                    class="purple-input"
                    required
                    @click:append="show1 = !show1"
                    @input="$v.password.$touch()"
                    @blur="$v.password.$touch()"
                  />
                </v-col>

                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="repeatPassword"
                    :append-icon="show2 ? 'mdi-eye' : 'mdi-eye-off'"
                    :error-messages="repeatPasswordErrors"
                    :type="show2 ? 'text' : 'password'"
                    label="비밀번호 확인"
                    class="purple-input"
                    required
                    @click:append="show2 = !show2"
                    @input="$v.repeatPassword.$touch()"
                    @blur="$v.repeatPassword.$touch()"
                  />
                </v-col>

                <v-col cols="12" md="4">
                  <v-text-field
                    v-model="age"
                    :error-messages="ageErrors"
                    label="나이"
                    class="purple-input"
                    required
                    number
                    @input="$v.age.$touch()"
                    @blur="$v.age.$touch()"
                  />
                </v-col>

                <v-col cols="12" md="4">
                  <v-select
                    v-model="select"
                    :items="items"
                    :error-messages="selectErrors"
                    label="성별"
                    class="purple-input"
                    required
                    @change="$v.select.$touch()"
                    @blur="$v.select.$touch()"
                  />
                </v-col>

                <v-col cols="12" class="text-right">
                  <v-btn color="success" class="mr-4" @click="submit">
                    회원가입
                  </v-btn>
                </v-col>
              </v-row>
            </v-container>
          </v-form>
        </material-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { validationMixin } from "vuelidate";
import {
  required,
  sameAs,
  maxLength,
  minLength,
  email,
  between,
} from "vuelidate/lib/validators";
import { mapActions } from "vuex";
import MaterialCard from "@/components/MaterialCard";
export default {
  components: {
    MaterialCard,
  },
  mixins: [validationMixin],
  validations: {
    username: { required, minLength: minLength(3), maxLength: maxLength(10) },
    email: { required, email },
    password: { required, minLength: minLength(6) },
    repeatPassword: {
      sameAsPassword: sameAs("password"),
    },
    age: { required, between: between(1, 150) },
    select: { required },
  },
  data: () => ({
    username: "",
    email: "",
    password: "",
    repeatPassword: "",
    show1: false,
    show2: false,
    age: 0,
    select: null,
    items: ["남", "여"],
  }),
  computed: {
    usernameErrors() {
      const errors = [];
      if (!this.$v.username.$dirty) return errors;
      !this.$v.username.maxLength &&
        errors.push("아이디는 3 - 10 글자 사이의 길이여야 합니다.");
      !this.$v.username.minLength &&
        errors.push("아이디는 3 - 10 글자 사이의 길이여야 합니다.");
      !this.$v.username.required && errors.push("아이디를 입력해주세요.");
      return errors;
    },
    selectErrors() {
      const errors = [];
      if (!this.$v.select.$dirty) return errors;
      !this.$v.select.required && errors.push("성별을 골라주세요.");
      return errors;
    },
    ageErrors() {
      const errors = [];
      if (!this.$v.age.$dirty) return errors;
      !this.$v.age.between && errors.push("정확한 나이를 입력해주세요.");
      !this.$v.age.required && errors.push("나이를 입력해주세요.");
      return errors;
    },
    emailErrors() {
      const errors = [];
      if (!this.$v.email.$dirty) return errors;
      !this.$v.email.email && errors.push("E-mail 형식이 아닙니다.");
      !this.$v.email.required && errors.push("E-mail을 입력해주세요.");
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
    repeatPasswordErrors() {
      const errors = [];
      if (!this.$v.repeatPassword.$dirty) return errors;
      !this.$v.repeatPassword.sameAsPassword &&
        errors.push("비밀번호가 다릅니다.");
      !this.$v.password.required && errors.push("비밀번호를 입력해주세요.");
      return errors;
    },
  },
  methods: {
    ...mapActions("data", ["signUp"]),
    submit() {
      this.$v.$touch();
      if (this.$v.$invalid) {
        return;
      }
      const user = {
        username: this.username,
        email: this.email,
        password: this.password,
      };
      const params = {
        user,
        age: this.age,
        gender: this.select,
      };
      this.signUp(params);
    },
  },
};
</script>
