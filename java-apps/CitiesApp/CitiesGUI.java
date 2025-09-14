import javax.swing.*;
import javax.swing.table.DefaultTableModel;
import java.awt.*;
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;

public class CitiesGUI extends JFrame {
    private List<City> cities;

    public CitiesGUI() {
        super("Cities Viewer");
        cities = loadCities("../data/cities.txt");
        setupUI();
    }

    private List<City> loadCities(String path) {
        List<City> list = new ArrayList<>();
        try (BufferedReader reader = new BufferedReader(
                new InputStreamReader(new FileInputStream(path), StandardCharsets.UTF_8))) {
            String line;
            while ((line = reader.readLine()) != null) {
                String[] parts = line.split("#");
                if (parts.length == 11) {
                    String ref = parts[0];
                    String nameGR = parts[1];
                    String gender = parts[8];
                    String nameEN = parts[9];
                    String state = parts[10];
                    list.add(new City(ref, nameGR, gender, nameEN, state));
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        return list;
    }

    private void setupUI() {
        setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
        String[] columns = {"Greek Name", "Gender", "English Name", "State"};
        DefaultTableModel model = new DefaultTableModel(columns, 0);
        for (City c : cities) {
            model.addRow(new Object[]{c.getNameGR(), c.getGender(), c.getNameEN(), c.getState()});
        }
        JTable table = new JTable(model);
        add(new JScrollPane(table), BorderLayout.CENTER);
        setSize(600, 400);
        setLocationRelativeTo(null);
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> new CitiesGUI().setVisible(true));
    }
}
