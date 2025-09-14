import javax.swing.*;
import javax.swing.table.DefaultTableModel;
import java.awt.*;
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;

public class NamedEntitiesGUI extends JFrame {
    private List<NamedEntity> entities;

    public NamedEntitiesGUI() {
        super("Named Entities Viewer");
        entities = loadEntities("../data/namedEntities.txt");
        setupUI();
    }

    private List<NamedEntity> loadEntities(String path) {
        List<NamedEntity> list = new ArrayList<>();
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
                    String type = parts[10];
                    list.add(new NamedEntity(ref, nameGR, gender, nameEN, type));
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        return list;
    }

    private void setupUI() {
        setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
        String[] columns = {"Greek Name", "Gender", "English Name", "Type"};
        DefaultTableModel model = new DefaultTableModel(columns, 0);
        for (NamedEntity e : entities) {
            model.addRow(new Object[]{e.getNameGR(), e.getGender(), e.getNameEN(), e.getType()});
        }
        JTable table = new JTable(model);
        add(new JScrollPane(table), BorderLayout.CENTER);
        setSize(700, 400);
        setLocationRelativeTo(null);
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> new NamedEntitiesGUI().setVisible(true));
    }
}
