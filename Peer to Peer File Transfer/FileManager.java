import java.io.BufferedInputStream;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Random;
import java.util.Scanner;
import java.util.StringTokenizer;

public class FileManager {
	// ********* 클라이언트 쓰레드와 서버 쓰레드의 정보들을 관리하는 클래스 *********** //
	final int BUFFER_SIZE = 10240;		// 한 번에 옮길 수 있는 청크크기
	int chunkNum;						// 청크의 개수
	String filename;					// 파일 이름
	String filePath;					// 파일 저장 경로
	String[] ipArr;						// configuration file의 IP모음
	int peerNum;						// 연결 할 Peer의 번호(가변)
	int ownNum;							// 자신의 Peer번호(불변)
	int[] portArr;						// configuration file의 port모음
	int[] numOfDown;					// 각 피어마다 파일을 주고 받은 횟수
	byte[] buffer;						// 청크를 닮을 그릇
	String bitMap;						// 각 Peer에 대한 bitMap
	boolean[] isSeeder;					// 각 Peer의 Seeder 유무
	
	FileManager(int peerNum) {
		this.peerNum = peerNum;
		this.ownNum = peerNum;
		this.bitMap = "";
		this.portArr = new int[5];
		this.ipArr = new String[5];
		this.buffer = new byte[BUFFER_SIZE];
		this.numOfDown = new int[5];
		this.isSeeder = new boolean[5];
	}
	public String getFilePath() {
		return this.filePath;
	}
	public void setFilename(String filename) {
		this.filename = filename;
	}
	public String getFilename() {
		return this.filename;
	}
	public int getNumDown() {
		return numOfDown[ownNum];
	}
	public void plusNumOfDown() {
		numOfDown[ownNum]++;
	}
	public void initNumOfDown() {
		this.numOfDown[ownNum] = 0;
	}
	public boolean isSeeder() {
		return isSeeder[ownNum];
	}
	public String getBitMap() {
		return this.bitMap;
	}
	
	public int getOwnNum() {
		return this.ownNum;
	}
	public int getPeerPort() {
		return this.portArr[peerNum];
	}
	public String getPeerIp() {
		return this.ipArr[peerNum];
	}
	
	// ************** 연결할 Peer번호 선택 (순차적으로 증가)************* //
	public void setConnectPeerNum() {
		// 통신할 peer를 순차적으로 선택
		if(this.peerNum >= 0 && this.peerNum <= 3)
			this.peerNum++;
		else if(this.peerNum == 4) 
			this.peerNum = 0;
		
		// 자기 자신과는 통신하지 않기 때문에 peerNum을 하나씩 증가
		if(this.peerNum == ownNum) {
			if(this.peerNum >= 0 && this.peerNum <= 3)
				this.peerNum++;
			else if(this.peerNum == 4) 
				this.peerNum = 0;
		}
	}
	
	// ************** 모든 청크를 받아서 bitMap이 모두 1인지 확인 ************* //
	public boolean isChunkFull() {
		if (chunkNum == 0) return false;
		for (int i = 0; i < bitMap.length(); i++) {
			if (bitMap.charAt(i) == '0')
				return false;
		}
		return true;
	}
	
	// ************** Peer의 번호에 따른 다른 저장경로 ************* //
	public void setFilePath() {			
		switch(ownNum) {
		case 0: this.filePath = "C:\\Users\\김효일\\eclipse-workspace\\Project4\\P2P\\src\\Peer1\\"; break;
		case 1: this.filePath = "C:\\Users\\김효일\\eclipse-workspace\\Project4\\P2P\\src\\Peer2\\"; break;
		case 2: this.filePath = "C:\\Users\\김효일\\eclipse-workspace\\Project4\\P2P\\src\\Peer3\\"; break;
		case 3: this.filePath = "C:\\Users\\김효일\\eclipse-workspace\\Project4\\P2P\\src\\Peer4\\"; break;
		case 4: this.filePath = "C:\\Users\\김효일\\eclipse-workspace\\Project4\\P2P\\src\\Peer5\\"; break;
		default: break;
		} 
	}
	
	// ************** chunk저장 후 bitMap 갱신 ************* //
	public void updateBitMap(int missIndex) {
		if (missIndex == bitMap.length() - 1)
			bitMap = bitMap.substring(0, missIndex) + "1";
		else
			bitMap = bitMap.substring(0, missIndex) + "1" + bitMap.substring(missIndex + 1);
	}
	
	// ************** leecher들의 bitMap 초기화(chunk 개수 만큼 0을 가짐, ex - 00000)  ************* //
	public void initLeecherBitMap() {
		StringBuffer s = new StringBuffer();
		for (int i = 0; i < chunkNum; i++) {
			s.append("0");
		}
		bitMap = s.toString();
	}

	// ************** Seeder bitMap 갱신(chunk 개수 만큼 1을 가짐, ex - 111111) ************* //
	public void initSeederBitMap() throws IOException {
		File file = new File(filePath + filename);
		FileInputStream fis = new FileInputStream(file);
		BufferedInputStream bis = new BufferedInputStream(fis);	
		this.chunkNum = (int)Math.ceil((double)file.length() / BUFFER_SIZE);
		
		for (int i = 0; i < chunkNum; i++) {
			if(bis.read(buffer) != -1) {
				bitMap = bitMap.substring(0, i) + "1";
			} else {
				break;
			}
		}
		isSeeder[peerNum] = true;
		bis.close();
		fis.close();
	}
}
