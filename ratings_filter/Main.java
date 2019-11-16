import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.InputStreamReader;
import java.util.*;

public class Main {

    public static void main(String[] args) throws Exception {
        File fileMetadata = new File("movies_metadata.csv");
        BufferedReader br = new BufferedReader(new FileReader(fileMetadata));
        StringTokenizer st = new StringTokenizer(br.readLine(),",");
        String line;
        // Get the titles of the movies from movies_metadata.csv
        // java Main < movies_metadata.csv > titles.csv
        ArrayList<String> titles = new ArrayList<>();
        st.nextToken();
        for (int i = 0; i < 469172 + 1; i++) {
            titles.add("");
        }
        while ((line = br.readLine()) != null) {
            // Remove conflicting text
            line = line.replaceAll("[\"][^\"]*[\"]", "");
            // Fix commas formatting (needs an space between)
            while (line.contains(",,")) {
                line = line.replaceAll("[,]{2}", ", ,");
            }
            st = new StringTokenizer(line,",");
            // Elude problem caused by bad format
            // Ensure that is reading the start of an entry
            if(st.nextToken().equals("False")) {
                st.nextToken();
                st.nextToken();
                st.nextToken();
                st.nextToken();
                int id = Integer.parseInt(st.nextToken());
                st.nextToken();
                st.nextToken();
                String title = st.nextToken();
                titles.set(id, title);
            }
        }

        File fileRatings = new File("ratings.csv");
        br = new BufferedReader(new FileReader(fileRatings));
        st = new StringTokenizer(br.readLine(),",");
        st.nextToken();
        CounterList moviesRatingsCounter = new CounterList();
        RatingsMatrix ratingsMatrix = new RatingsMatrix();
        while ((line = br.readLine()) != null) {
            st = new StringTokenizer(line,",");
            int userId = Integer.parseInt(st.nextToken());
            int movieId = Integer.parseInt(st.nextToken());
            double rating = Double.parseDouble(st.nextToken());

            moviesRatingsCounter.count(movieId);
            ratingsMatrix.addRating(userId, movieId, rating);

            //userMovieRating.put(new Pair<>(userId,movieId),rating);
        }
        ArrayList<Integer> movieIds = moviesRatingsCounter.top(20);
        double[][] ratings = ratingsMatrix.getRatingsMatrix(50, movieIds);

        File fileLinks = new File("links.csv");
        br = new BufferedReader(new FileReader(fileLinks));
        st = new StringTokenizer(br.readLine(),",");
        st.nextToken();
        ArrayList<Integer> moviesIdRelations = new ArrayList<>();
        for (int i = 0; i < 176279 + 1; i++) {
            moviesIdRelations.add(0);
        }
        while ((line = br.readLine()) != null) {
            st = new StringTokenizer(line,",");
            int movieId = Integer.parseInt(st.nextToken());
            st.nextToken();
            if (st.hasMoreTokens()) {
                int tmdbId = Integer.parseInt(st.nextToken());
                moviesIdRelations.add(movieId, tmdbId);
            }
        }

        for (int movieId : movieIds) {
            String movieTitle = titles.get(moviesIdRelations.get(movieId));
            System.out.println(movieTitle);
        }

        for (int i = 0; i < ratings.length; i++) {
            for (int j = 0; j < ratings[0].length - 1; j++) {
                System.out.print(ratings[i][j]+ " ");
            }
            System.out.print(ratings[i][ratings[0].length - 1] + "\n");
        }

        //System.out.println(ratingsMatrix.getUserIds());
        //System.out.println(movieIds);
        //System.out.println(Arrays.deepToString(ratings));

    }

    public static class Pair<K,V> {
        private K key;
        private V value;

        public Pair(K key, V value) {
            this.key = key;
            this.value = value;
        }

        public K getKey() {
            return key;
        }

        public V getValue() {
            return value;
        }

        public void setKey(K key) {
            this.key = key;
        }

        public void setValue(V value) {
            this.value = value;
        }

        @Override
        public int hashCode() {
            int hash = 7;
            hash = 31 * hash + key.hashCode();
            hash = 31 * hash + value.hashCode();
            return hash;
        }

        @Override
        public boolean equals(Object obj) {
            if (obj instanceof Pair) {
                Pair p = (Pair) obj;
                return this.key.equals(p.getKey()) && this.value.equals(p.getValue());
            }
            return false;
        }
    }

    public static class CounterList {
        ArrayList<Integer> ids;
        ArrayList<Integer> quantities;

        public CounterList() {
            this.ids = new ArrayList<>();
            this.quantities = new ArrayList<>();
        }

        public void count(int id) {
            if (!this.ids.contains(id)) {
                this.ids.add(id);
                this.quantities.add(1);
            }
            else {
                int index = this.ids.indexOf(id);
                this.quantities.set(index, this.quantities.get(index) + 1);
            }
        }

        public ArrayList<Integer> top(int limit) {
            ArrayList<Integer> idsTop = new ArrayList<>();
            ArrayList<Integer> quantitiesOrdered = new ArrayList<>(this.quantities);

            quantitiesOrdered.sort(Integer::compareTo);
            for (int i = 1; i < limit+1; i++) {
                int q = quantitiesOrdered.get(quantitiesOrdered.size() - i);
                int index = this.quantities.indexOf(q);
                idsTop.add(this.ids.get(index));
                this.quantities.remove(index);
                this.ids.remove(index);
            }
            return idsTop;
        }
    }

    public static class RatingsMatrix {
        HashMap<Pair<Integer,Integer>,Double> userMovieRating;
        ArrayList<Integer> userIds;

        public RatingsMatrix() {
            this.userMovieRating = new HashMap<>();
            this.userIds = null;
        }

        public void addRating(int userId, int movieId, double rating) {
            this.userMovieRating.put(new Pair<>(userId, movieId), rating);
        }

        public double[][] getRatingsMatrix(int limit, ArrayList<Integer> movieIds) {
            CounterList userRatingsCounter = new CounterList();
            for (Pair<Integer,Integer> userMovie: this.userMovieRating.keySet()) {
                if (movieIds.contains(userMovie.getValue())) {
                    userRatingsCounter.count(userMovie.getKey());
                }
            }
            this.userIds = userRatingsCounter.top(limit);

            double[][] ratings = new double[limit][movieIds.size()];
            for (int i = 0; i < limit; i++) {
                int u = this.userIds.get(i);
                for (int j = 0; j < movieIds.size(); j++) {
                    int m = movieIds.get(j);
                    Double rating = this.userMovieRating.get(new Pair<>(u,m));
                    if (rating != null) {
                        ratings[i][j] = rating;
                    }
                    else {
                        ratings[i][j] = 0;
                    }
                }
            }
            
            return ratings;
        }

        public ArrayList<Integer> getUserIds() {
            return this.userIds;
        }
    }
}
