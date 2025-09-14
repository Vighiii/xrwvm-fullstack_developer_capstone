public class NamedEntity {
    private String ref;
    private String nameGR;
    private String gender;
    private String nameEN;
    private String type;

    public NamedEntity(String ref, String nameGR, String gender, String nameEN, String type) {
        this.ref = ref;
        this.nameGR = nameGR;
        this.gender = gender;
        this.nameEN = nameEN;
        this.type = type;
    }

    public String getRef() { return ref; }
    public String getNameGR() { return nameGR; }
    public String getGender() { return gender; }
    public String getNameEN() { return nameEN; }
    public String getType() { return type; }
}
