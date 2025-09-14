public class City {
    private String ref;
    private String nameGR;
    private String gender;
    private String nameEN;
    private String state;

    public City(String ref, String nameGR, String gender, String nameEN, String state) {
        this.ref = ref;
        this.nameGR = nameGR;
        this.gender = gender;
        this.nameEN = nameEN;
        this.state = state;
    }

    public String getRef() { return ref; }
    public String getNameGR() { return nameGR; }
    public String getGender() { return gender; }
    public String getNameEN() { return nameEN; }
    public String getState() { return state; }
}
