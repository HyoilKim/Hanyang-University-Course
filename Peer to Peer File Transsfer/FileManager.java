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
	// ********* Ŭ���̾�Ʈ ������� ���� �������� �������� �����ϴ� Ŭ���� *********** //
	final int BUFFER_SIZE = 10240;		// �� ���� �ű� �� �ִ� ûũũ��
	int chunkNum;						// ûũ�� ����
	String filename;					// ���� �̸�
	String filePath;					// ���� ���� ���
	String[] ipArr;						// configuration file�� IP����
	int peerNum;						// ���� �� Peer�� ��ȣ(����)
	int ownNum;							// �ڽ��� Peer��ȣ(�Һ�)
	int[] portArr;						// configuration file�� port����
	int[] numOfDown;					// �� �Ǿ�� ������ �ְ� ���� Ƚ��
	byte[] buffer;						// ûũ�� ���� �׸�
	String bitMap;						// �� Peer�� ���� bitMap
	boolean[] isSeeder;					// �� Peer�� Seeder ����
	
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
	
	// ************** ������ Peer��ȣ ���� (���������� ����)************* //
	public void setConnectPeerNum() {
		// ����� peer�� ���������� ����
		if(this.peerNum >= 0 && this.peerNum <= 3)
			this.peerNum++;
		else if(this.peerNum == 4) 
			this.peerNum = 0;
		
		// �ڱ� �ڽŰ��� ������� �ʱ� ������ peerNum�� �ϳ��� ����
		if(this.peerNum == ownNum) {
			if(this.peerNum >= 0 && this.peerNum <= 3)
				this.peerNum++;
			else if(this.peerNum == 4) 
				this.peerNum = 0;
		}
	}
	
	// ************** ��� ûũ�� �޾Ƽ� bitMap�� ��� 1���� Ȯ�� ************* //
	public boolean isChunkFull() {
		if (chunkNum == 0) return false;
		for (int i = 0; i < bitMap.length(); i++) {
			if (bitMap.charAt(i) == '0')
				return false;
		}
		return true;
	}
	
	// ************** Peer�� ��ȣ�� ���� �ٸ� ������ ************* //
	public void setFilePath() {			
		switch(ownNum) {
		case 0: this.filePath = "C:\\Users\\��ȿ��\\eclipse-workspace\\Project4\\P2P\\src\\Peer1\\"; break;
		case 1: this.filePath = "C:\\Users\\��ȿ��\\eclipse-workspace\\Project4\\P2P\\src\\Peer2\\"; break;
		case 2: this.filePath = "C:\\Users\\��ȿ��\\eclipse-workspace\\Project4\\P2P\\src\\Peer3\\"; break;
		case 3: this.filePath = "C:\\Users\\��ȿ��\\eclipse-workspace\\Project4\\P2P\\src\\Peer4\\"; break;
		case 4: this.filePath = "C:\\Users\\��ȿ��\\eclipse-workspace\\Project4\\P2P\\src\\Peer5\\"; break;
		default: break;
		} 
	}
	
	// ************** chunk���� �� bitMap ���� ************* //
	public void updateBitMap(int missIndex) {
		if (missIndex == bitMap.length() - 1)
			bitMap = bitMap.substring(0, missIndex) + "1";
		else
			bitMap = bitMap.substring(0, missIndex) + "1" + bitMap.substring(missIndex + 1);
	}
	
	// ************** leecher���� bitMap �ʱ�ȭ(chunk ���� ��ŭ 0�� ����, ex - 00000)  ************* //
	public void initLeecherBitMap() {
		StringBuffer s = new StringBuffer();
		for (int i = 0; i < chunkNum; i++) {
			s.append("0");
		}
		bitMap = s.toString();
	}

	// ************** Seeder bitMap ����(chunk ���� ��ŭ 1�� ����, ex - 111111) ************* //
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