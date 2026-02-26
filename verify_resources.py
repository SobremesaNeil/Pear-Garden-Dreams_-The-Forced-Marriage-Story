#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ren'Py 视觉小说资源完整性验证脚本
用于扫描所有 .rpy 文件中引用的音频和图像资源，并检查这些资源是否存在。
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Tuple, Set


class ResourceVerifier:
    """资源验证器类"""
    
    def __init__(self, game_dir: str = "game"):
        """
        初始化验证器
        
        Args:
            game_dir: 游戏目录的相对路径
        """
        self.game_dir = Path(game_dir)
        self.images_dir = self.game_dir / "images"
        self.audio_dir = self.game_dir / "audio"
        
        # 用于存储和图像的错误信息
        self.audio_errors: Dict[str, List[Tuple[str, int]]] = {}
        self.image_errors: Dict[str, List[Tuple[str, int]]] = {}
        
        # 用于统计
        self.total_audio_files = 0
        self.total_image_files = 0
        self.audio_files_found = 0
        self.image_files_found = 0
    
    def get_all_rpy_files(self) -> List[Path]:
        """获取 game 目录下的所有 .rpy 文件"""
        rpy_files = []
        if self.game_dir.exists():
            for rpy_file in self.game_dir.glob("*.rpy"):
                rpy_files.append(rpy_file)
            # 递归查找子目录中的 .rpy 文件（除了 cache 和 tl）
            for root, dirs, files in os.walk(self.game_dir):
                # 排除 cache 和 tl 目录
                dirs[:] = [d for d in dirs if d not in ['cache', 'tl']]
                for file in files:
                    if file.endswith('.rpy'):
                        rpy_path = Path(root) / file
                        if rpy_path not in rpy_files:
                            rpy_files.append(rpy_path)
        return sorted(rpy_files)
    
    def get_existing_image_basenames(self) -> Set[str]:
        """
        扫描 game/images 目录，获取所有图像文件的无后缀名称
        例如: bg backstage_1.jpg -> "bg backstage_1"
        """
        image_names = set()
        if self.images_dir.exists():
            for image_file in self.images_dir.iterdir():
                if image_file.is_file():
                    # 获取文件的无后缀名称
                    name_without_ext = image_file.stem
                    image_names.add(name_without_ext)
        return image_names
    
    def get_existing_audio_files(self) -> Set[str]:
        """
        扫描 game/audio 目录，获取所有音频文件的相对路径集合
        """
        audio_files = set()
        if self.audio_dir.exists():
            for audio_file in self.audio_dir.iterdir():
                if audio_file.is_file():
                    # 存储相对于 game 目录的路径
                    rel_path = f"audio/{audio_file.name}"
                    audio_files.add(rel_path)
        return audio_files
    
    def extract_audio_calls(self, file_path: Path) -> List[Tuple[str, int, str]]:
        """
        从 .rpy 文件中提取所有音频调用
        返回: [(音频路径, 行号, 完整调用语句), ...]
        """
        audio_calls = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # 正则表达式：匹配 play music/sound/audio "path" 或 'path'
            # 支持可选的 fadein/fadeout 参数
            pattern = r'play\s+(music|sound|audio)\s+["\']([^"\']+)["\']'
            
            for line_num, line in enumerate(lines, 1):
                stripped = line.strip()
                # 跳过注释行
                if stripped.startswith('#'):
                    continue
                
                matches = re.finditer(pattern, line)
                for match in matches:
                    audio_path = match.group(2)
                    audio_calls.append((audio_path, line_num, stripped))
        
        except UnicodeDecodeError:
            print(f"⚠️  无法读取文件（编码问题）: {file_path}")
        except Exception as e:
            print(f"⚠️  读取文件时出错: {file_path} - {e}")
        
        return audio_calls
    
    def extract_image_calls(self, file_path: Path) -> List[Tuple[str, int, str]]:
        """
        从 .rpy 文件中提取所有图像调用（scene 和 show）
        提取的是核心标签，丢弃 with 和 at 后的内容
        返回: [(图像标签, 行号, 完整调用语句), ...]
        """
        image_calls = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # 正则表达式：匹配 scene/show 语句
            # scene bg_name [at position] [with transition]
            # show character_name [at position] [with transition]
            
            # 更精确的模式：
            # 1. scene 开头，提取到第一个 "with" 或 "at" 或行尾
            # 2. show 开头，提取到第一个 "with" 或 "at" 或行尾
            
            for line_num, line in enumerate(lines, 1):
                line_stripped = line.strip()
                
                # 跳过注释和空行
                if not line_stripped or line_stripped.startswith("#"):
                    continue
                
                # 处理 scene 语句
                if line_stripped.startswith("scene "):
                    # 分离出核心部分（丢弃 with 和 at 后的内容）
                    core_part = line_stripped[6:]  # 移除 "scene "
                    # 找到第一个 with 或 at（不区分大小写）
                    core_part = re.split(r'\s+(with|at)\s+', core_part)[0].strip()
                    
                    # 过滤掉特殊值如 "black", "None" 等
                    if core_part and core_part not in ['black', 'None', 'none', '']:
                        image_calls.append((core_part, line_num, line_stripped))
                
                # 处理 show 语句
                elif line_stripped.startswith("show "):
                    # 分离出核心部分
                    core_part = line_stripped[5:]  # 移除 "show "
                    # 找到第一个 with 或 at
                    core_part = re.split(r'\s+(with|at)\s+', core_part)[0].strip()
                    
                    # 过滤掉特殊值如 "screen" 等
                    if core_part and not core_part.startswith("screen "):
                        image_calls.append((core_part, line_num, line_stripped))
        
        except UnicodeDecodeError:
            print(f"⚠️  无法读取文件（编码问题）: {file_path}")
        except Exception as e:
            print(f"⚠️  读取文件时出错: {file_path} - {e}")
        
        return image_calls
    
    def verify_audio_resources(self) -> None:
        """验证所有音频资源"""
        print("\n" + "="*80)
        print("🎵 音频资源验证中...")
        print("="*80)
        
        rpy_files = self.get_all_rpy_files()
        existing_audio = self.get_existing_audio_files()
        
        all_audio_found = set()
        all_audio_missing = {}
        
        for rpy_file in rpy_files:
            audio_calls = self.extract_audio_calls(rpy_file)
            
            for audio_path, line_num, full_line in audio_calls:
                self.total_audio_files += 1
                
                # 标准化路径（确保使用正斜杠）
                normalized_path = audio_path.replace("\\", "/")
                
                # 检查文件是否存在
                full_path = self.game_dir / normalized_path
                if full_path.exists():
                    self.audio_files_found += 1
                    all_audio_found.add(normalized_path)
                else:
                    # 记录缺失的文件
                    if normalized_path not in all_audio_missing:
                        all_audio_missing[normalized_path] = []
                    all_audio_missing[normalized_path].append((rpy_file.name, line_num))
        
        # 输出结果
        if all_audio_missing:
            print(f"\n❌ 找到 {len(all_audio_missing)} 个缺失的音频文件：\n")
            for audio_name, locations in sorted(all_audio_missing.items()):
                print(f"  【缺失】 {audio_name}")
                for file_name, line_num in locations:
                    print(f"          └─ {file_name}:{line_num}")
            self.audio_errors = all_audio_missing
        else:
            print(f"\n✅ 所有 {self.total_audio_files} 个音频文件都存在！")
    
    def verify_image_resources(self) -> None:
        """验证所有图像资源"""
        print("\n" + "="*80)
        print("🖼️  图像资源验证中...")
        print("="*80)
        
        rpy_files = self.get_all_rpy_files()
        existing_images = self.get_existing_image_basenames()
        
        all_images_found = set()
        all_images_missing = {}
        
        for rpy_file in rpy_files:
            image_calls = self.extract_image_calls(rpy_file)
            
            for image_tag, line_num, full_line in image_calls:
                self.total_image_files += 1
                
                # 检查图像是否存在
                if image_tag in existing_images:
                    self.image_files_found += 1
                    all_images_found.add(image_tag)
                else:
                    # 记录缺失的文件
                    if image_tag not in all_images_missing:
                        all_images_missing[image_tag] = []
                    all_images_missing[image_tag].append((rpy_file.name, line_num))
        
        # 输出结果
        if all_images_missing:
            print(f"\n❌ 找到 {len(all_images_missing)} 个缺失的图像文件：\n")
            for image_name, locations in sorted(all_images_missing.items()):
                print(f"  【缺失】 {image_name}")
                for file_name, line_num in locations:
                    print(f"          └─ {file_name}:{line_num}")
            self.image_errors = all_images_missing
        else:
            print(f"\n✅ 所有 {self.total_image_files} 个图像文件都存在！")
    
    def print_summary(self) -> None:
        """打印汇总报告"""
        print("\n" + "="*80)
        print("📊 汇总报告")
        print("="*80)
        
        # 统计信息
        print(f"\n📁 项目结构：")
        print(f"   - 游戏目录: {self.game_dir.absolute()}")
        print(f"   - 图像目录: {self.images_dir.absolute()}")
        print(f"   - 音频目录: {self.audio_dir.absolute()}")
        
        print(f"\n🔍 扫描结果：")
        rpy_files = self.get_all_rpy_files()
        print(f"   - 扫描的 .rpy 文件数: {len(rpy_files)}")
        print(f"   - 图像资源检查: {self.image_files_found}/{self.total_image_files}")
        print(f"   - 音频资源检查: {self.audio_files_found}/{self.total_audio_files}")
        
        # 最终结论
        print("\n" + "="*80)
        if not self.audio_errors and not self.image_errors:
            if self.total_audio_files > 0 or self.total_image_files > 0:
                print("🎉 资产体检完成：所有代码调用的外部资源均已就位！")
            else:
                print("⚠️  未检测到任何资源调用")
        else:
            total_errors = len(self.audio_errors) + len(self.image_errors)
            print(f"⚠️  发现 {total_errors} 个资源问题，请立即修复！")
        print("="*80 + "\n")
    
    def run(self) -> bool:
        """
        执行完整的验证流程
        返回: 如果没有错误返回 True，有错误返回 False
        """
        print("\n")
        print("╔" + "="*78 + "╗")
        print("║" + " "*78 + "║")
        print("║" + "Ren'Py 视觉小说资源完整性验证工具".center(78) + "║")
        print("║" + " "*78 + "║")
        print("╚" + "="*78 + "╝")
        
        self.verify_audio_resources()
        self.verify_image_resources()
        self.print_summary()
        
        return len(self.audio_errors) == 0 and len(self.image_errors) == 0


def main():
    """主函数"""
    # 获取当前工作目录
    current_dir = Path.cwd()
    print(f"当前工作目录: {current_dir}")
    
    # 查找 game 目录
    game_dir = current_dir / "game"
    if not game_dir.exists():
        print(f"❌ 错误：找不到 game 目录在 {current_dir}")
        print("   请确保在项目根目录运行此脚本")
        return False
    
    # 创建验证器并运行
    verifier = ResourceVerifier("game")
    success = verifier.run()
    
    return success


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
