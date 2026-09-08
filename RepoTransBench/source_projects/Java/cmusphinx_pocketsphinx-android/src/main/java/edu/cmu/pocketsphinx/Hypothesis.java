package edu.cmu.pocketsphinx;

public class Hypothesis {
    private final String text;
    private final int score;

    public Hypothesis(String text, int score) {
        this.text = text;
        this.score = score;
    }

    public String getHypstr() { return text; }
    public int getBestScore() { return score; }
}