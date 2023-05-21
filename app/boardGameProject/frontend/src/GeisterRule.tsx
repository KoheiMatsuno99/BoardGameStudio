import React from "react";
import styles from "./GeisterRule.module.css";
import Lobby from "./Lobby";

const GeisterRule: React.FC = () => {
    const [doesGoBack, setGoback] = React.useState(false);
    const [doesPlay, setPlay] = React.useState(false);
    const handleGoback = () => {
        setGoback(true);
    }
    const handlePlay = () => {
        setPlay(true);
    }
    return (
        doesGoBack ? <Lobby /> : 
        (
            <div className={styles.container}>
                <div>
                    <h1>ガイスターのルール</h1>
                    <p>ガイスターは、2人で遊ぶボードゲームです。</p>
                    <p>ゲームの目的は、相手のゴーストを捕まえることです。</p>
                    <p>ゴーストは、赤と青の2色があります。ただし、相手のコマの種類はコマを取るまでわかりません。</p>
                    <p>各プレイヤーは、青いオバケと赤いオバケのコマをそれぞれ4つずつ持っています。</p>
                    <p>ゲーム開始時に各プレイヤーは手前の8マスに8つの自分のコマを自由に配置します。</p>
                    <p>配置が終わったら、先手のプレイヤーから交互にコマを1つ動かします。</p>
                    <p>コマは、自分のコマを1マス前後左右に動かすことができます。</p>
                    <p>ただし、移動先に自分のコマがある時はその移動先には動かすことができません。</p>
                    <p>進めた先に相手のコマがある場合は、そのコマを取らなければなりません。</p>
                    <p>各プレイヤーから見て相手側の一番奥のマスは脱出マスとなっています。</p>
                    <p>自分のコマが脱出マスに到達し、その次のターンで相手に取られなければ、そのコマをボードから脱出させることができます。</p>
                    <p>勝利条件は、「相手の青いオバケを全て取る」「自分の赤いオバケを全て取らせる」「自分の青いオバケを1つでも脱出させる」のどれかを満たすことです。</p>
                </div>
                <div className={styles.buttonArea}>
                    <button className={styles.button} onClick={handleGoback}>Go Back</button>
                    <button className={styles.button} onClick={handlePlay}>Play</button>
                </div>           
            </div>
        )
        
    )
}

export default GeisterRule;